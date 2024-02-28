import logging
import asyncio
import aiofiles
import argparse
import textwrap
from datetime import datetime
from contextlib import asynccontextmanager
from environs_processing import get_env_contents


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            '''
            Script for connecting to chat via TCP/UPD.
            Reads live chat messages and displays
            them in the terminal. Allows save messages history to a file.
            '''
        )
    )
    parser.add_argument('--host', type=str, help='chat hostname')
    parser.add_argument('--read-port', type=int, help='chat port number for reading messages')
    parser.add_argument('--history', default='messages.txt', type=str, help='chating history')
    return parser.parse_args()


async def write_to_file(filepath, message):
    async with aiofiles.open(filepath, 'a') as file:
        await file.write(message)


@asynccontextmanager
async def connect_to_chat(host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        yield reader, writer
    except ConnectionError as err:
        logging.error(f'{err}')
    except asyncio.CancelledError:
        logging.error('Cancelled.')
    except Exception as err:
        logging.error(f'{err}')
    finally:
        writer.close()
        logging.debug('Close the connection.')
        await writer.wait_closed()


async def read_chat_messages(host, port, filepath):
    async with connect_to_chat(host, port) as connection:
        while True:
            reader, writer = connection[0], connection[1]
            data = await reader.read(1024)
            if not data:
                break
            message = f'{data.decode()!r}'
            date_now = f"[{datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M')}]"
            print(date_now, message)
            await write_to_file(filepath, f'{date_now} {message}\n')


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='py_log.log',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s'
    )

    args = vars(parse_arguments())
    environs = get_env_contents()
    host = args.get('host') or environs['host']
    port = args.get('read_port') or environs['read_port']
    filepath = args.get('filepath') or environs['filepath']

    asyncio.run(read_chat_messages(host, port, filepath))


if __name__ == '__main__':
    main()
