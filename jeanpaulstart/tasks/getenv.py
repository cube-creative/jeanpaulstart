import logging
from jeanpaulstart import environment
from jeanpaulstart.constants import *


TASK_COMMAND = 'getenv'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    splitted['arguments'] = {'file': splitted['arguments']}
    return splitted


def apply_(file):
    with open( file, 'rb' ) as f:
        for line in f.readlines():
            line = line.strip().decode( 'utf-8' )
            key, value = line.split( '=', 1 )

            key = key.strip()
            value = value.strip()
            if not len( key ) or key[ 0 ] == '=':
                continue

            environment.set( key, value )
            logging.info( '[From %s] %s=%s', TASK_COMMAND, key, value )
    return OK
