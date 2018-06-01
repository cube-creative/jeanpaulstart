__all__ = [
    'load_plugins',
    'run_batch',
    'run_from_json',
    'run_from_filepath',
    'dump_data_for_command_line',
    'dump_file_for_command_line',
    'batches_from_folders',
    'batches_for_user',
    'AsyncExecutor'
]
from jeanpaulstart import batch
from jeanpaulstart import executor
from jeanpaulstart import plugin_loader
from jeanpaulstart.async_executor import AsyncExecutor
from jeanpaulstart.constants import *


def load_plugins():
    """
    Initialize the plugin loader
    """
    plugin_loader.init(force=True)


def run_batch(batch_data):
    """
    Runs the given batch data
    :param batch_data: data
    :return: registered status
    """
    return executor.run_batch(batch_data)


def run_from_json(json_content, normalized=True):
    """
    Given a JSON content, runs the batch
    :param json_content: JSON String
    :param normalized: has the JSON data been normalized yet ?
    :return: registered status
    """
    status, batch_ = batch.from_json(json_content, normalized)

    if status is not OK:
        return status

    return executor.run_batch(batch_)


def run_from_filepath(filepath):
    """
    Runs batch from  a given filepath (json or yaml)
    :param filepath: String
    :return: registered status
    """
    batch_ = batch.from_filepath(filepath)

    if batch_ is None:
        return

    return executor.run_batch(batch_)


def dump_data_for_command_line(data, normalize=True):
    """
    Prepares data for command line use
    :param data: batch data
    :param normalize: should the data be normalized ?
    :return: string
    """
    return batch.dump_data_for_command_line(data, normalize)


def dump_file_for_command_line(filepath, normalize=True):
    """
    Prepares data from  a given filepath for command line use
    :param filepath: filepath
    :param normalize: should the data be normalized ?
    :return: string
    """
    return batch.dump_file_for_command_line(filepath, normalize)


def batches_from_folders(folders):
    """
    Returns all the batches found in a given folder
    :param folders: string
    :return: list of batches
    """
    return batch.from_folders(folders)


def batches_for_user(batch_directories, tags_filepath, username):
    """zef
    Tralalal afze
    :param batch_directories:
    :param tags_filepath:
    :param username:
    :return:
    """
    return batch.from_folders_for_user(batch_directories, tags_filepath, username)
