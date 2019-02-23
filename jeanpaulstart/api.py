from .constants import *
from . import batch as _batch
#import batch as _batch
from .executor import Executor, run_batch
from . import plugin_loader as _plugin_loader


Batch = _batch.Batch


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

    return run_batch(batch)


def executor_from_filepath(filepath):
    """
    Return an Executor from a given batch filepath
    :param filepath: Path to a batch file
    :return: Executor
    """
    batch = Batch(filepath=filepath)
    executor = Executor(batch)
    return executor


def batches_from_folders(folders):
    """
    Loads all the batches in given folders
    :param folders: A list of folders
    :return: A list of successfully loaded batches
    """
    return _batch.from_folders(folders)


def batches_for_user(batch_directories, tags_filepath, username):
    """
    Loads all the batches in given folders, with matching tags for given tags file and username
    :param batch_directories: A list of folders
    :param tags_filepath: The filepath to the tags definition file
    :param username: The username
    :return: A list of successfully loaded batches
    """
    return _batch.from_folders_for_user(batch_directories, tags_filepath, username)
