from jeanpaulstart.constants import *


TASK_COMMAND = 'command-name'


def validate(user_data):
    return OK, "message"


def normalize_after_split(splitted):
    normalized = {
        'name': 'Some Task',
        'command': 'command-name',
        'arguments': {
            'arg1' : 'value1'
        },
        'ignore_errors': False
    }

    return normalized


def apply_(name, arguments):
    pass
