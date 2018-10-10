import logging
from task import Task
from jeanpaulstart.constants import *
from jeanpaulstart import plugin_loader


plugin_loader.init()


def _catch_exception(task_data):
    if 'ignore_errors' in task_data.keys():
        logging.info(
            "Task '{name}' : 'ignore_errors' has been renamed to 'catch_exception', "
            "please update your batch".format(
                name=task_data['name']
        ))
        return task_data['ignore_errors']

    return task_data.get('catch_exception', False)


def _register_status(task_data):
    return task_data.get('register_status', False)


def _exit_if_not_ok(task_data):
    if task_data.get('ignore_errors', False) or task_data.get('catch_exception', False):
        logging.info("Task '{name}' : 'exit_if_not_ok' defaults to false since catch_exception=true".format(
            name=task_data['name']
        ))
        return False

    if 'abort_on_failure' in task_data.keys():
        logging.info(
            "Task '{name}' : 'abort_on_failure' has been renamed to 'exit_if_not_ok', "
            "please update your batch".format(
                name=task_data['name']
        ))
        return task_data['abort_on_failure']

    return task_data.get('exit_if_not_ok', True)


def _when(task_data):
    return str(task_data.get('when', True))


def _prepare_task_data(task_data):
    command_name = task_data.keys()[1]

    splitted = {
        'name': task_data['name'],
        'command': command_name,
        'arguments': task_data[command_name],
        'catch_exception': _catch_exception(task_data),
        'register_status': _register_status(task_data),
        'exit_if_not_ok': _exit_if_not_ok(task_data),
        'when': _when(task_data)
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
    task.catch_exception = task_data['catch_exception']
    task.register_status = task_data['register_status']
    task.exit_if_not_ok = task_data['exit_if_not_ok']
    task.when = task_data['when']

    return task


def normalize(data):
    tags = normalize_tags(data['tags'])
    tasks = list()
    status = OK

    tasks += normalize_environment(data.get('environment', dict()))
    tasks += [normalize_task(task) for task in data['tasks']]

    return tags, tasks, status
