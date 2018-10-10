from jeanpaulstart import file_io
from jeanpaulstart.constants import *


TASK_COMMAND = 'copy'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    splitted['arguments']['force'] = splitted['arguments'].get('force', True)
    return splitted


def apply_(src, dest, force):
    file_io.copy(src, dest, force)

    return OK
