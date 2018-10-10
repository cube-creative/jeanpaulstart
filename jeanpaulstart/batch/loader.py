from batch import Batch
from jeanpaulstart import tags
from jeanpaulstart import parser
from jeanpaulstart.constants import *


def from_folders(folders):
    """
    Loads all the batches in given folders
    :param folders: A list of folders
    :return: A list of successfully loaded batches
    """
    batches = list()

    for filepath in parser.from_folders(folders):
        batch = Batch(filepath=filepath)
        if batch.load_status == OK:
            batches.append(batch)

    return batches


def from_folders_for_user(batch_directories, tags_filepath, username):
    """
    Loads all the batches in given folders, with matching tags for given tags file and username
    :param batch_directories: A list of folders
    :param tags_filepath: The filepath to the tags definition file
    :param username: The username
    :return: A list of successfully loaded batches
    """
    user_batches = list()
    batches = from_folders(batch_directories)
    user_tags = set(tags.load_by_user(tags_filepath, username))

    for batch_ in batches:
        if not user_tags.isdisjoint(batch_.tags):
            user_batches.append(batch_)

    return user_batches
