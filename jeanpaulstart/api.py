from .constants import *
from .batch import Batch
from .executor import Executor, run_batch
from . import plugin_loader as _plugin_loader


def load_plugins():
    """
    Initializes the plugin loader
    """
    _plugin_loader.init(force=True)


def run_from_filepath(filepath):
    """
    Runs batch from  a given filepath (json or yaml)
    :param filepath: String
    :return: BATCH_NO_DATA, BATCH_NOT_VALID, BATCH_NOT_NORMALIZED or Executor's registered status
    """
    batch = Batch(filepath=filepath)

    if batch.load_status != OK:
        return batch.load_status

    status, messages = run_batch(batch)
    return status


def executor_from_filepath(filepath):
    batch = Batch(filepath)
    executor = Executor(batch)
    return executor
