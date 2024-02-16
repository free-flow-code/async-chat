import logging
import asyncio
from environs_processing import fetch_environs


async def send_message(host, port, message):
    try:
        reader, writer = await asyncio.open_connection(f'{host}', port)
        writer.write(f'{message}\n\n'.encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()
    except ConnectionError as err:
        logging.error(f'{err}')
    except asyncio.CancelledError:
        logging.error('Cancelled.')
    except Exception as err:
        logging.error(f'{err}')


def main():
    logging.getLogger('asyncio').setLevel(logging.DEBUG)
    environs = fetch_environs()
    host = environs['host']
    port = environs['send_port']
    message = environs['message']

    if not message:
        message = input('Введите сообщение: ')

    asyncio.run(send_message(host, port, message))


if __name__ == '__main__':
    main()
