import logging
from jeanpaulstart.constants import *
from jeanpaulstart import plugin_loader


plugin_loader.init()


def _validate_name(data):
    if 'name' not in data.keys():
        return VALID_NAME_MISSING, ""

    if not (isinstance(data['name'], str) or isinstance(data['name'], unicode)):
        return VALID_NAME_NOT_STRING, ""

    return OK, ""


def _validate_icon(data):
    if 'icon_path' not in data.keys():
        return VALID_ICON_MISSING, ""

    return OK, ""


def _validate_tags(data):
    if 'tags' not in data.keys():
        return VALID_TAGS_MISSING, ""

    if not isinstance(data['tags'], list):
        return VALID_TAGS_NOT_LIST, ""

    return OK, ""


def _validate_task(task_data):
    command_name = task_data.keys()[1]
    task_plugin = plugin_loader.loaded_plugins.get(command_name, None)

    if not task_plugin:
        return VALID_TASK_PLUGIN_NOT_FOUND, "[{task_name}] No plugin found for command '{command_name}'".format(
            task_name=task_data['name'],
            command_name=command_name
        )

    return task_plugin.validate(task_data)


def _validate_tasks(data):
    if 'tasks' not in data.keys():
        return VALID_TASKS_MISSING, ""

    if not isinstance(data['tasks'], list):
        return VALID_TASKS_NOT_LIST, ""

    for task in data['tasks']:
        status, message = _validate_task(task)
        if status is not OK:
            return status, message

    return OK, ""


def validate(data):
    status, message = _validate_name(data)
    if status is not OK: return status, message

    status, message = _validate_icon(data)
    if status is not OK: return status, message

    status, message = _validate_tags(data)
    if status is not OK: return status, message

    status, message = _validate_tasks(data)
    if status is not OK: return status, message

    return OK, ""
