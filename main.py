import os
import asyncio
import aiofiles
import argparse
from environs import Env
from datetime import datetime

env = Env()
env.read_env()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Message chat.')
    parser.add_argument('--host', default='', type=str, help='chat hostname')
    parser.add_argument('--port', type=int, help='chat port number')
    parser.add_argument('--history', default='messages.txt', type=str, help='chating history')
    return parser.parse_args()


async def write_to_file(filepath, message):
    async with aiofiles.open(filepath, 'a') as file:
        await file.write(message)


async def read_chat_messages(host, port, filepath):
    try:
        reader, writer = await asyncio.open_connection(f'{host}', port)

        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = f'{data.decode()!r}'
            date_now = f"[{datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M')}]"
            print(date_now, message)
            await write_to_file(filepath, f'{date_now} {message}\n')

        print('Close the connection')
        writer.close()
        await writer.wait_closed()
    except ConnectionError as err:
        print(f'Connection error: {err}')
    except asyncio.CancelledError:
        print('Cancelled')
    except Exception as err:
        print(f'Unexpected error: {err}')


def main():
    if os.path.isfile('.env'):
        host = env.str('HOST')
        port = env.int('PORT')
        filepath = env.str('HISTORY', 'messages.txt')
    else:
        args = parse_arguments()
        host = args.host
        port = args.port
        filepath = args.history

    asyncio.run(read_chat_messages(host, port, filepath))


if __name__ == '__main__':
    main()
