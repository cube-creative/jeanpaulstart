from jeanpaulstart import file_io
from jeanpaulstart.constants import *


TASK_COMMAND = 'file'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    return splitted


def apply_(path, state):
    if state == STATE_DIRECTORY:
        file_io.mkdir(path)
    elif state == STATE_ABSENT:
        file_io.remove(path)
    return OK
