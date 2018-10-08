from jeanpaulstart import file_io
from jeanpaulstart.constants import *


TASK_COMMAND = 'copy'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    splitted['arguments']['force'] = splitted['arguments'].get('force', True)
    return splitted


def apply_(src, dest, force):
    if file_io.copy(src, dest, force) is None:
        return STATE_ALREADY_EXISTS

    return OK
