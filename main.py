import asyncio
import aiofiles
from datetime import datetime


async def write_to_file(filename, message):
    async with aiofiles.open(filename, 'a') as file:
        await file.write(message)


async def read_chat_messages(host, port):
    reader, writer = await asyncio.open_connection(f'{host}', port)
    filename = 'messages.txt'

    while True:
        data = await reader.read(1024)
        message = f'{data.decode()!r}'
        date_now = f"[{datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M')}]"
        print(date_now, message)
        await write_to_file(filename, f'{date_now} {message}\n')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


def main():
    host = 'minechat.dvmn.org'
    port = 5000
    asyncio.run(read_chat_messages(host, port))


if __name__ == '__main__':
    main()
