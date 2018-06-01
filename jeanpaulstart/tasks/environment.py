from jeanpaulstart import environment
from jeanpaulstart.constants import *


TASK_COMMAND = 'environment'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    return splitted


def apply_(name, value):
    environment.set_env_variable(name, value)
