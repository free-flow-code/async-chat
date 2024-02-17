import os
import json
import logging
import asyncio
import aiofiles
import argparse
import textwrap
from environs_processing import get_env_contents


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            '''
            Script for connecting to chat via TCP/UPD.
            Sends a message to the chat. Allows you to
            register and log in using a token.
            '''
        )
    )
    parser.add_argument('message', type=str, help='message sent to chat')
    parser.add_argument('--host', type=str, help='chat hostname')
    parser.add_argument('--send-port', type=int, help='chat port number for sending messages')
    parser.add_argument('--token', type=str, help='authorized token for connection to chat')
    parser.add_argument('--username', type=str, help='username for registration')
    return parser.parse_args()


def escape_control_symbols(string):
    return string.replace('\n', '')


async def authorise(reader, writer, token):
    writer.write(f'{token}\n'.encode())
    await writer.drain()

    response_message = await reader.readline()
    assert json.loads('null') is None
    authorise_data = json.loads(response_message.decode())

    return authorise_data


async def register(reader, writer, username):
    username = username or input('Введите желаемое имя: ')
    writer.write(f'{escape_control_symbols(username)}\n'.encode())

    account_data = await reader.readline()
    async with aiofiles.open('account_data.json', mode='w') as file:
        await file.write(account_data.decode())

    return json.loads(account_data.decode())


async def submit_message(writer, message):
    writer.write(f'{message}\n'.encode())
    await writer.drain()


async def connect_to_chat(host, port, message, token, username):
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
            if await register(reader, writer, username):
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

    args = vars(parse_arguments())
    environs = get_env_contents()
    message = args.get('message')
    host = args.get('host') or environs.get('host')
    port = args.get('send_port') or environs.get('send_port')
    token = args.get('token') or environs.get('token')
    username = args.get('username') or environs.get('username')

    asyncio.run(connect_to_chat(host, port, escape_control_symbols(message), token, username))


if __name__ == '__main__':
    main()
