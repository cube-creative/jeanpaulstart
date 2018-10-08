import jeanpaulstart
from jeanpaulstart.constants import *


TASK_COMMAND = 'include_tasks'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    return splitted


def apply_(file):
    status = jeanpaulstart.run_from_filepath(file)

    if status is None:
        return 1

    return status
