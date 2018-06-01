import os
import logging
from jeanpaulstart import environment
from jeanpaulstart import plugin_loader
from jeanpaulstart.constants import *


plugin_loader.init()


def apply_(task_dict, batch_name="Unknown Batch"):
    command = task_dict['command']
    arguments = environment.parse_env_variables_from_dict(task_dict['arguments'])
    command_apply = plugin_loader.loaded_plugins[command].apply_

    logging.info("[{batch_name}][{task_name}] '{command}' with argument(s) {arguments}".format(
        batch_name=batch_name,
        task_name=task_dict['name'],
        command=command,
        arguments=" ".join(["%s=%s" % (key, value) for key, value in arguments.items()])
    ))

    if task_dict['ignore_errors'] in [True, 'yes']:
        try:
            command_apply(**arguments)
            status = OK

        except Exception, exception:
            logging.info("[{batch_name}][{task_name}][**IGNORED ERROR**] {e}".format(
                batch_name=batch_name,
                task_name=task_dict['name'],
                e=exception)
            )
            status = ERROR_IGNORED
    else:
        status = command_apply(**arguments)

    return status


def run_batch(batch):
    logging.info("[{batch_name}][Begin batch run]".format(batch_name=batch['name']))
    logging.info("[{batch_name}][Backup environment]".format(batch_name=batch['name']))
    environment_backup = dict(os.environ)

    task_runned = 0
    ignored_errors = 0
    registered_status = OK

    for task in batch['tasks']:
        status = apply_(task, batch['name'])

        if task['register_status']:
            logging.info("[{batch_name}][{task_name}] Registering status for exit code: '{status}'".format(
                batch_name=batch['name'],
                task_name=task['name'],
                status=status
            ))
            registered_status = status

        if status is ERROR_IGNORED:
            ignored_errors += 1

        task_runned += 1

    logging.info("[{batch_name}][Restore environment]".format(batch_name=batch['name']))
    os.environ.clear()
    os.environ.update(environment_backup)

    logging.info(
        "[{batch_name}][End batch run] {task_runned:03d} task(s) runned, {ignored_errors:03d} ignored errors".format(
            task_runned=task_runned,
            ignored_errors=ignored_errors,
            batch_name=batch['name']
    ))

    return registered_status
