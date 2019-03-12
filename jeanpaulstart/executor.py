import os
import logging
import collections
from . import environment
from . import plugin_loader
from .constants import *


def _apply_(task):
    """
    Applies a given task
    :param task: A task
    :return: status, a list of messages
    """
    arguments = environment.parse(task.arguments)
    plugin = plugin_loader.loaded_plugins.get(task.command_name, None)
    if 'async_' in task.arguments:
        value = task.arguments.__getitem__('async_')
        task.arguments.__setitem__('async', value)
        task.arguments.__delitem__('async_')
    messages = ["[{task_name}] '{command_name}' with argument(s) {arguments}".format(
        task_name=task.name,
        command_name=task.command_name,
        arguments=' '.join(['{0}={1}'.format(key, value) for key, value in task.arguments.items()])
    )]

    when = (environment.parse_expression(task.when))
    if not eval(when):
        messages.append('[{task_name}][**SKIPPED**] when clause evaluated to False : {clause}'.format(
            task_name=task.name,
            clause=task.when
        ))
        status = TASK_WHEN_FALSE
        return status, messages

    if task.catch_exception:
        try:
            plugin.apply_(**arguments)
            status = OK

        except Exception as exception:
            messages.append('[{task_name}][**IGNORED ERROR**] {error}'.format(
                task_name=task.name,
                error=exception
            ))
            status = TASK_ERROR_IGNORED

    else:
        status = plugin.apply_(**arguments)

    return status, messages


class Executor(object):
    """
    Run batches tasks, set by step or as a whole
    """
    def __init__(self, batch):
        self.batch = batch
        self.status = EXEC_IDLE
        self._messages = list()
        self._message_index = 0
        self._task_index = 0
        self._ignored_errors = 0
        self._registered_status = None
        self._environment_backup = dict()

        if self.batch.load_status != OK:
            logging.info('Given batch is not loaded : ' + self.batch.load_status)
            self.status = BATCH_NOT_LOADED

    def __repr__(self):
        return "Executor(batch={batch}, status={status})".format(
            batch=self.batch,
            status=self.status
        )

    def _step_messages(self):
        self._message_index = len(self._messages)

    def _post_messages(self, messages):
        [logging.info(message) for message in messages]
        self._messages += messages

    @property
    def progress(self):
        """
        Property that returns the progress of execution as a float [0..1]
        :return: float
        """
        return float(self._task_index) / len(self.batch.tasks)

    @property
    def messages(self):
        """
        Property that return all the messages the tasks generated during execution
        :return: a list of string
        """
        return self._messages

    @property
    def last_messages(self):
        """
        Property that returns the list of last added messages (i.e for the latest task applied)
        :return: a list of messages
        """
        return self._messages[self._message_index:]

    def reset(self):
        """
        Resets execution infos (status, messages, current task, ignored errors,
        registered status, environment backup)
        :return:
        """
        self._messages = list()
        self._task_index = 0
        self._ignored_errors = 0
        self._registered_status = OK
        self._environment_backup = dict()
        os.environ[EXEC_REGISTERED_STATUS_ENV_VAR] = str(OK)

    @property
    def next_task(self):
        """
        Property that returns the next task that will be applied
        (useful for displaying Ui messages before execution)
        :return: The next task, None if execution finished of Batch not OK
        """
        if self._task_index >= len(self.batch.tasks):
            return

        return self.batch.tasks[self._task_index]

    def _backup_environment(self):
        self._environment_backup = dict(os.environ)

    def _restore_environment(self):
        os.environ.clear()
        os.environ.update(self._environment_backup)

    def _begin(self):
        self._post_messages(['[{}] Begin'.format(self.batch.name)])

        if self.batch.load_status == BATCH_NOT_LOADED:
            self._abort('Init', 'Batch is not loaded')
            self.status = EXEC_BEGIN_FAILED
            return

        if self.batch.load_status == BATCH_NOT_VALID:
            self._abort('Init', 'Batch is not valid')
            self.status = EXEC_BEGIN_FAILED
            return

        if self.batch.load_status == BATCH_NOT_NORMALIZED:
            self._abort('Init', 'Batch is not normalized')
            self.status = EXEC_BEGIN_FAILED
            return

        self.status = EXEC_RUNNING
        self.reset()
        self._backup_environment()

    def _finish(self):
        self._post_messages(['[{name}] Finished (tasks={tasks}, errors_ignored={errors})'.format(
            name=self.batch.name,
            tasks=len(self.batch.tasks),
            errors=self._ignored_errors
        )])
        self.status = EXEC_FINISHED
        self._restore_environment()

    def _abort(self, step_name, reason):
        self._post_messages(['[{batch_name}][{step_name}][**ABORT**] {reason}'.format(
            batch_name=self.batch.name,
            step_name=step_name,
            reason=reason
        )])
        self.status = EXEC_ABORTED
        self._restore_environment()

    def step(self):
        """
        Applies the next available task
        :return: status, a list of new messages
        """
        self._step_messages()

        if self.status == EXEC_IDLE:
            self._begin()

        if self.has_stopped:
            return self.status

        current_task = self.batch.tasks[self._task_index]
        self._task_index += 1

        status, messages = _apply_(current_task)
        self._post_messages(['[{0}]{1}'.format(self.batch.name, message) for message in messages])

        if status == TASK_ERROR_IGNORED:
            self._ignored_errors += 1

        if current_task.register_status and status != TASK_WHEN_FALSE:
            self._registered_status = status
            os.environ[EXEC_REGISTERED_STATUS_ENV_VAR] = str(status)

        if current_task.exit_if_not_ok and status not in (OK, TASK_WHEN_FALSE):
            self._abort(current_task.name, 'Status was not OK and exit_if_not_ok=true')

        if self._task_index >= len(self.batch.tasks):
            self._finish()

        return status, self.last_messages

    @property
    def has_stopped(self):
        """
        Helper property to check execution was aborted or finished
        :return:  True or False
        """
        return self.status in (EXEC_FINISHED, EXEC_ABORTED, EXEC_BEGIN_FAILED, BATCH_NOT_LOADED)

    @property
    def success(self):
        """
        Helper property to check if execution went well
        :return: True or False
        """
        return self.status == EXEC_FINISHED

    def run_all(self):
        """
        Runs the whole batch
        :return: registered status, a list of all messages
        """
        self.reset()

        while not self.has_stopped:
            self.step()

        return self._registered_status, self._messages, self.status


def run_batch(batch):
    """
    Runs the given batch
    :param batch: a valid and normalized batch
    :return: registered status, list of messages, executor status
    """
    executor = Executor(batch)
    registered_status, messages, executor_status = executor.run_all()

    if executor.success:
        return registered_status

    return executor_status
