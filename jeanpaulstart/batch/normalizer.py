import copy
from jeanpaulstart import plugin_loader
from jeanpaulstart.constants import *


plugin_loader.init()


def _ignore_errors(task_dict):
    return task_dict.get('ignore_errors', False)


def _register_status(task_dict):
    return task_dict.get('register_status', False)


def _split_keys_and_deep_copy(task):
    command_name = task.keys()[1]

    splitted = {
        'name': task['name'],
        'command': command_name,
        'arguments': task[command_name],
        'ignore_errors': _ignore_errors(task),
        'register_status': _register_status(task)
    }

    return copy.deepcopy(splitted)


def _make_task_from_environment(name, value):
    task_dict = {
        'name': 'From environment',
        'command': 'environment',
        'arguments': {
            'name': name,
            'value': value
        },
        'ignore_errors': False,
        'register_status': False
    }
    return task_dict


def normalize_environment(environment):
    tasks = list()

    for name, value in environment.items():
        task_dict = _make_task_from_environment(name, value)
        tasks.append(task_dict)

    return tasks


def normalize_tags(tags):
    tags = list(tags)
    if TAG_ADMIN not in tags:
        tags.append(TAG_ADMIN)
    return tags


def normalize_task(task_dict):
    splitted = _split_keys_and_deep_copy(task_dict)
    command = splitted['command']

    if command in plugin_loader.loaded_plugins.keys():
        return plugin_loader.loaded_plugins[command].normalize_after_split(splitted)

    return splitted


def normalize_batch(batch_data):
    normalized = batch_data.copy()

    normalized['tags'] = normalize_tags(batch_data['tags'])

    if 'environment' in batch_data.keys(): normalized.pop('environment')

    environment_tasks = normalize_environment(batch_data.get('environment', dict()))
    normalized['tasks'] = environment_tasks + [normalize_task(task) for task in batch_data['tasks']]

    return normalized
