from jeanpaulstart import plugin_loader
from jeanpaulstart.constants import *


plugin_loader.init()


def _validate_name(data):
    if 'name' not in data.keys():
        return NAME_MISSING, ""

    if not (isinstance(data['name'], str) or isinstance(data['name'], unicode)):
        return NAME_NOT_STRING, ""

    return OK, ""


def _validate_icon(data):
    if 'icon_path' not in data.keys():
        return ICON_MISSING, ""

    return OK, ""


def _validate_tags(data):
    if 'tags' not in data.keys():
        return TAGS_MISSING, ""

    if not isinstance(data['tags'], list):
        return TAGS_NOT_LIST, ""

    return OK, ""


def _validate_task(task):
    command_name = task.keys()[1]
    task_plugin = plugin_loader.loaded_plugins.get(command_name, None)

    if not task_plugin:
        return TASK_PLUGIN_NOT_FOUND, "No plugin found for task '{command_name}'".format(command_name=command_name)

    return task_plugin.validate(task)


def _validate_tasks(data):
    if 'tasks' not in data.keys():
        return TASKS_MISSING, ""

    if not isinstance(data['tasks'], list):
        return TASKS_NOT_LIST, ""

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
