import jeanpaulstart
from jeanpaulstart.constants import *


TASK_COMMAND = 'include_tasks'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    normalized = dict(splitted)
    normalized['arguments']['preserve_env'] = splitted['arguments'].get('preserve_env', False)
    return normalized


def apply_(file, preserve_env):
    return jeanpaulstart.run_from_filepath(file, preserve_env)
