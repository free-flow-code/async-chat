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
        print(f'Connection error: {err}')
    except asyncio.CancelledError:
        print('Cancelled')
    except Exception as err:
        print(f'Unexpected error: {err}')


def main():
    environs = fetch_environs()
    host = environs['host']
    port = environs['send_port']
    message = environs['message']

    if not message:
        message = input('Введите сообщение: ')

    asyncio.run(send_message(host, port, message))


if __name__ == '__main__':
    main()
