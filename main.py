import asyncio


async def connect_to_chat(host, port):
    reader, writer = await asyncio.open_connection(f'{host}', port)

    while True:
        data = await reader.read(1024)
        message = f'{data.decode()!r}'
        print(message)
        with open('messages.txt', 'a') as file:
            file.write(f'{message}\n')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


def main():
    host = 'minechat.dvmn.org'
    port = 5000
    asyncio.run(connect_to_chat(host, port))


if __name__ == '__main__':
    main()
