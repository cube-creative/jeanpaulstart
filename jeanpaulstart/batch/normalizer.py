from task import Task
from jeanpaulstart.constants import *
from jeanpaulstart import plugin_loader


plugin_loader.init()


def _ignore_errors(task_data):
    return task_data.get('ignore_errors', False)


def _register_status(task_data):
    return task_data.get('register_status', False)


def _abort_on_failure(task_data):
    return task_data.get('abort_on_failure', False)


def _prepare_task_data(task_data):
    command_name = task_data.keys()[1]

    splitted = {
        'name': task_data['name'],
        'command': command_name,
        'arguments': task_data[command_name],
        'ignore_errors': _ignore_errors(task_data),
        'register_status': _register_status(task_data),
        'abort_on_failure': _abort_on_failure(task_data)
    }

    return splitted


def _make_task_from_environment(name, value):
    task = Task(
        name='From environment',
        command_name='environment',
        arguments={'name': name, 'value': value}
    )

    return task


def normalize_tags(tags):
    if TAG_ADMIN not in tags:
        tags.append(TAG_ADMIN)
    return tags


def normalize_environment(environment_data):
    for name, value in environment_data.items():
        task = _make_task_from_environment(name, value)
        yield task


def normalize_task(task_data):
    task_data = _prepare_task_data(task_data)
    task_data = plugin_loader.loaded_plugins[task_data['command']].normalize_after_split(task_data)

    task = Task(
        name=task_data['name'],
        command_name=task_data['command'],
        arguments=task_data['arguments']
    )
    task.ignore_errors = task_data['ignore_errors']
    task.register_status = task_data['register_status']
    task.abort_on_failure = task_data['abort_on_failure']

    return task


def normalize(data):
    tags = normalize_tags(data['tags'])
    tasks = list()
    status = OK

    tasks += normalize_environment(data.get('environment', list()))
    tasks += [normalize_task(task) for task in data['tasks']]

    return tags, tasks, status
