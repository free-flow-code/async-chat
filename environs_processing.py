import os
import argparse
from environs import Env

env = Env()
env.read_env()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Message chat.')
    parser.add_argument('--host', default='', type=str, help='chat hostname')
    parser.add_argument('--read-port', type=int, help='chat port number for reading messages')
    parser.add_argument('--send-port', type=int, help='chat port number for sending messages')
    parser.add_argument('--history', default='messages.txt', type=str, help='chating history')
    parser.add_argument('--message', default='', type=str, help='message sent to chat')
    return parser.parse_args()


def fetch_environs():
    args = parse_arguments()

    if args.message:
        message = args.message
    else:
        message = None

    if os.path.isfile('.env'):
        host = env.str('HOST')
        read_port = env.int('READ_PORT')
        send_port = env.int('SEND_PORT')
        filepath = env.str('HISTORY', 'messages.txt')
    else:
        host = args.host
        read_port = args.read_port
        send_port = args.send_port
        filepath = args.history

    return {
        'host': host,
        'read_port': read_port,
        'send_port': send_port,
        'filepath': filepath,
        'message': message
    }


if __name__ == '__main__':
    fetch_environs()
