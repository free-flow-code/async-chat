import os
import json
import logging
import asyncio
import aiofiles
from environs_processing import fetch_environs


async def authorise(reader, writer, token):
    writer.write(f'{token}\n'.encode())
    await writer.drain()

    response_message = await reader.readline()
    assert json.loads('null') is None
    authorise_data = json.loads(response_message.decode())

    return authorise_data


async def register(reader, writer):
    username = input('Введите желаемое имя: ')
    writer.write(f'{username}\n'.encode())

    account_data = await reader.readline()
    async with aiofiles.open('account_data.json', mode='w') as file:
        await file.write(account_data.decode())

    return json.loads(account_data.decode())


async def submit_message(writer, message):
    writer.write(f'{message}\n'.encode())
    await writer.drain()


async def connect_to_chat(host, port, message, token):
    try:
        reader, writer = await asyncio.open_connection(f'{host}', port)
        answer = await reader.readline()
        logging.debug(answer.decode())

        if not token and os.path.isfile('account_data.json'):
            async with aiofiles.open('account_data.json', mode='r') as file:
                file_content = await file.read()
                account_data = json.loads(file_content)
                token = account_data['account_hash']

        if not await authorise(reader, writer, token):
            logging.debug('Неизвестный токен. Регистрация нового пользователя.')
            if await register(reader, writer):
                logging.debug('Новый аккаунт зарегистрирован. Данные записаны в файл.')

        await submit_message(writer, message)
        logging.debug('Сообщение отправлено.')
        writer.close()
        await writer.wait_closed()

    except json.JSONDecodeError as err:
        logging.error(f'Ошибка при декодировании JSON: {err}', exc_info=True)
    except ConnectionError as err:
        logging.error(f'Обрыв соединения: {err}')
    except asyncio.CancelledError:
        logging.error('Cancelled.')
    except Exception as err:
        logging.error(f'{err}', exc_info=True)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='py_log.log',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s'
    )
    environs = fetch_environs()
    host = environs.get('host')
    port = environs.get('send_port')
    message = environs.get('message')
    token = environs.get('token')

    if not message:
        message = input('Введите сообщение: ')

    asyncio.run(connect_to_chat(host, port, message, token))


if __name__ == '__main__':
    main()
