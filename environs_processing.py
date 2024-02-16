import os
import argparse
from environs import Env


def parse_arguments():
    parser = argparse.ArgumentParser(description='Message chat.')
    parser.add_argument('--host', type=str, help='chat hostname')
    parser.add_argument('--read-port', type=int, help='chat port number for reading messages')
    parser.add_argument('--send-port', type=int, help='chat port number for sending messages')
    parser.add_argument('--history', default='messages.txt', type=str, help='chating history')
    parser.add_argument('--message', type=str, help='message sent to chat')
    parser.add_argument('--token', type=str, help='authorized token for connection to chat')
    return parser.parse_args()


def get_env_contents():
    if os.path.isfile('.env'):
        env = Env()
        env.read_env()
        return {
            'host': env.str('HOST', None),
            'read_port': env.int('READ_PORT', None),
            'send_port': env.int('SEND_PORT', None),
            'filepath': env.str('HISTORY', None),
            'token': env.str('TOKEN', None)
        }
    return None


def fetch_environs():
    if get_env_contents():
        return get_env_contents()

    args = parse_arguments()
    return vars(args)
