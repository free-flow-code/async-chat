import os
import json
import logging
import asyncio
import aiofiles
from environs_processing import fetch_environs


async def send_message(host, port, message, token):
    try:
        reader, writer = await asyncio.open_connection(f'{host}', port)
        answer = await reader.readline()
        logging.debug(answer.decode())

        if not os.path.isfile('account_data.json'):
            writer.write("\n".encode())
            await writer.drain()
            await reader.readline()
            username = input('Введите желаемое имя: ')
            writer.write(f"{username}\n".encode())
            account_data = await reader.readline()
            logging.debug(account_data.decode())
            async with aiofiles.open('account_data.json', mode="w") as file:
                await file.write(account_data.decode())
            return

        if token:
            writer.write(f'{token}'.encode())
            await writer.drain()
            response_message = await reader.readline()
            assert json.loads('null') is None
            response_data = json.loads(response_message.decode())
            if response_data is None:
                logging.error('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
                return

        writer.write(f"{message}\n\n".encode())
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
    host = environs.get('host')
    port = environs.get('send_port')
    message = environs.get('message')
    token = environs.get('token')

    if not message:
        message = input('Введите сообщение: ')

    asyncio.run(send_message(host, port, message, token))


if __name__ == '__main__':
    main()
