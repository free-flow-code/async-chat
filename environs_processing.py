import os
from environs import Env


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
