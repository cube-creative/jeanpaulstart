import os
import math
import logging
from jeanpaulstart import environment
from jeanpaulstart import plugin_loader
from jeanpaulstart.constants import *


class AsyncExecutor(object):

    def __init__(self, batch):
        self.message_offset = 0

        self._batch = batch
        self._batch_name = self._batch['name']
        self._tasks = self._batch['tasks']

        self._task_index = 0
        self._task_runned = 0
        self._ignored_errors = 0
        self._registered_status = OK

        self._environment_backup = dict()

        self._status = ASYNC_EXEC_READY

    def _post_message(self, message):
        logging.info(message)
        self._last_message = message

    def _backup_environment(self):
        self._environment_backup = dict(os.environ)

    def _restore_environment(self):
        os.environ.clear()
        os.environ.update(self._environment_backup)

    def _task_message(self, offset=0):
        if self._task_index + offset >= len(self._tasks):
            return

        task = self._tasks[self._task_index + offset]
        arguments = environment.parse_env_variables_from_dict(task['arguments'])

        self._post_message("[{batch_name}][{task_name}] '{command}' with argument(s) {arguments}".format(
            batch_name=self._batch_name,
            task_name=task['name'],
            command=task['command'],
            arguments=" ".join(["%s=%s" % (key, value) for key, value in arguments.items()])
        ))

    def _apply_(self, task_dict, batch_name="Unknown Batch"):
        command = task_dict['command']
        arguments = environment.parse_env_variables_from_dict(task_dict['arguments'])
        command_apply = plugin_loader.loaded_plugins[command].apply_

        if task_dict['ignore_errors'] in [True, 'yes']:
            try:
                command_apply(**arguments)
                status = OK

            except Exception, exception:
                self._post_message("[{batch_name}][{task_name}][**IGNORED ERROR**] {e}".format(
                    batch_name=batch_name,
                    task_name=task_dict['name'],
                    e=exception)
                )
                status = ERROR_IGNORED
        else:
            status = command_apply(**arguments)

        return status

    def step(self):
        if self._task_index >= len(self._tasks):
            self._post_message("[{batch_name}][Backup environment]".format(batch_name=self._batch['name']))
            self._restore_environment()
            self._status = ASYNC_EXEC_FINISHED
            return OK

        self._task_message(self.message_offset)
        task = self._tasks[self._task_index]
        status = self._apply_(task, self._batch_name)
        self._task_index += 1
        return status

    def last_message(self):
        return self._last_message

    def status(self):
        return self._status

    def progress(self):
        return math.trunc(100 * float(self._task_index) / len(self._tasks)) / 100.0

    def start(self):
        self._status = ASYNC_EXEC_RUNNING
        self._post_message("[{batch_name}][Begin batch run]".format(batch_name=self._batch['name']))
        self._post_message("[{batch_name}][Backup environment]".format(batch_name=self._batch['name']))
        self._backup_environment()
        self._task_message(self.message_offset)
