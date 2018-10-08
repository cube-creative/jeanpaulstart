import logging
from jeanpaulstart import parser
from jeanpaulstart.constants import *
from validator import validate
from normalizer import normalize


class Batch(object):
    """
    Object holding tasks to be run

    Member `load_status` defaults to `BATCH_NOT_LOADED`
    Member `name` defaults to "Unnamed batch"
    Member `tags`
    Member `tasks`
    """
    def __init__(self, data=None, source=None, filepath=None):
        self.name = "Unnamed batch"

        if data is not None:
            logging.info('New batch from data')
            self._data = data
        elif source is not None:
            logging.info('New batch from source')
            self._data = parser.parse(source)
        elif filepath is not None:
            logging.info('New batch from file ' + filepath)
            self._data = parser.from_file(filepath)

        self.load_status = BATCH_NOT_LOADED
        self.tags = list()
        self.tasks = list()

        self._load()

    def _load(self):
        """
        Validates and normalizes Batch data
        Updates member `loaded_status` with `OK`, `BATCH_NO_DATA`, `BATCH_NOT_VALID` or `BATCH_NOT_NORMALIZED`
        :return: None
        """
        if self._data is None:
            logging.info('No data was found')
            self.load_status = BATCH_NO_DATA
            return

        status, message = validate(self._data)

        if status != OK:
            logging.info('Validation failed : ' + message)
            self.load_status = BATCH_NOT_VALID
            return

        self.name = self._data['name']
        tags, tasks, status = normalize(self._data)

        if status != OK:
            logging.info('Batch normalization failed')
            self.load_status = BATCH_NOT_NORMALIZED
            return

        self.tags = tags
        self.tasks = tasks
        self.load_status = OK
