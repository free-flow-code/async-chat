import asyncio
import aiofiles
from datetime import datetime
from environs_processing import fetch_environs


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
    environs = fetch_environs()
    host = environs['host']
    port = environs['read_port']
    filepath = environs['filepath']

    asyncio.run(read_chat_messages(host, port, filepath))


if __name__ == '__main__':
    main()
