# Асинхронный чат на Python

Состоит из двух скриптов позволяет подключаться к чату по TCP протоколу.

`read_chat_messages.py` - в live-режиме выводит сообщения чата в терминал.
Поддерживает сохранение истории сообщений в файл.

`send_messages.py` - отправляет сообщение в чат.
Поддерживает регистрацию и авторизацию по токену.

Все необходимые параметры можно задать либо с помощью переменных окружения,
либо аргументами командной строки.
Скрипты в первую очередь берут данные из аргументов командноя строки.
При отсутствии каких-либо аргументов - будут взяты значения из `.env` файла. 

## Подготовка окружения

Для запуска Python 3.10 должен быть установлен.
Установите необходимые библиотеки:

```
pip3 install -r requirements.txt
```

## Чтение сообщений

```
python3 read_chat_messages.py --host <chat_hostname> --read-port <port_number> --history <file_name>
```

Не имеет обязательных параметров. По умолчанию `--history = messages.txt`.
История сообщений будет сохранена в файле `messages.txt` рядом с файлом скрипта.
Можно указать свой путь и имя файла.

**Номера портов для чтения и отправления сообщений отличаются.**

## Отправление сообщений

```
python3 send_messages.py <some_message> --host <chat_hostname> --send-port <port_number>
```

Имеет один обязательный параметр - текст сообщения.

Необязательные параметры:
- `--host`
- `--send-port`
- `--token` - токен для авторизации в чате
- `--username` - желаемое имя пользователя для регистрации в чате, если `--token` не указан.

**Номера портов для чтения и отправления сообщений отличаются.**

## Переменные окружения

Создайте рядом с файлом скрипта `.env` файл следующего содержания:

```
HOST=<chat_hostname>
READ_PORT=<port_number>
SEND_PORT=<port_number>
HISTORY=<file_name>
TOKEN=<authorized_token>
USERNAME=<some_username>
```

`HISTORY` - название или путь к файлу, в котором будет сохранена история сообщений чата.

`TOKEN` - необязательный параметр для авторизации в чате.

`USERNAME` - желаемое имя пользователя для регистрации в чате, если `TOKEN` не указан.