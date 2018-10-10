from copy import deepcopy
from subprocess import call
from jeanpaulstart.constants import *


TASK_COMMAND = 'pip'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    normalized = deepcopy(splitted)
    normalized['arguments']['state'] = splitted['arguments'].get('state', STATE_PRESENT)
    return normalized


def apply_(name, state):
    command = "pip install {state}{name}".format(
        state='--upgrade ' if state == STATE_FORCE_REINSTALL else '',
        name=name
    )

    exit_code = call(command, shell=True)

    if exit_code == 0:
        return OK

    return exit_code
