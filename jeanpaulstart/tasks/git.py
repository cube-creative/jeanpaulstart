from jeanpaulstart.constants import *


TASK_COMMAND = 'git'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    splitted['arguments']['sub_directory'] = splitted['arguments'].get('sub_directory', None)
    return splitted


def apply_(url, destination, sub_directory):
    checkout_remote(url, destination, sub_directory)

    return OK


def checkout_remote(url, destination, sub_directory):
    pass
