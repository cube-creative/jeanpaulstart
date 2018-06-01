__all__ = [
    'from_json',
    'from_filepath',
    'from_folders',
    'from_folders_for_user',
    'dump_data_for_command_line',
    'dump_file_for_command_line'
]
import json
import logging
from jeanpaulstart import tags
from jeanpaulstart.batch import parser
from jeanpaulstart.batch import validator
from jeanpaulstart.batch import normalizer
from jeanpaulstart.constants import *


def _validate_and_normalize(batch_data, filepath="unknown file"):
    status, message = validator.validate(batch_data)
    if status is not "OK":
        logging.warn("Could not validate batch data from {filepath} ({status}: {message})".format(
            filepath=filepath,
            status=status,
            message=message
        ))
        return

    normalized = normalizer.normalize_batch(batch_data)
    return normalized


def from_json(json_content, already_normalized=True):
    batch_data = parser.from_json(json_content)

    if not already_normalized:
        status, message = validator.validate(batch_data)
        if status is not OK:
            logging.warn("Could not validate JSON data (status:{status})".format(status=status))
            return status, None

        batch = normalizer.normalize_batch(batch_data)
        return OK, batch

    else:
        return OK, batch_data


def from_filepath(filepath):
    batch_data = parser.from_file(filepath)

    if not batch_data:
        logging.warn("Could not load batch file : '{filepath}' (file missing ?)".format(filepath=filepath))
        return

    normalized = _validate_and_normalize(batch_data, filepath)
    return normalized


def from_folders(folders):
    batches = list()

    for batch_filepath, batch_data in parser.from_folders(folders):
        normalized = _validate_and_normalize(batch_data, batch_filepath)

        if not normalized: continue

        logging.info("Loaded batch : {filepath}".format(filepath=batch_filepath))
        batches.append(normalized)

    return batches


def from_folders_for_user(batch_directories, tags_filepath, username):
    batches = from_folders(batch_directories)
    user_tags = set(tags.load_by_user(tags_filepath, username))

    user_batches = list()
    for batch_ in batches:
        if not user_tags.isdisjoint(batch_['tags']):
            user_batches.append(batch_)

    return user_batches


def dump_data_for_command_line(data, normalize=True):
    if normalize:
        status, message = validator.validate(data)
        if status is not OK:
            logging.warn("Could not validate data for dumping (status={status})".format(status=status))
            return
        data = normalizer.normalize_batch(data)

    dumped = json.dumps(data)
    escaped = json.dumps(dumped)
    escaped_less = escaped.replace("\\\\\\\\", "\\\\")

    return escaped_less


def dump_file_for_command_line(filepath, normalize=True):
    data = parser.from_file(filepath)
    return dump_data_for_command_line(data, normalize)
