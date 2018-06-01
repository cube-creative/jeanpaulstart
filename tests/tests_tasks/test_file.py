import unittest
from copy import deepcopy
from jeanpaulstart.tasks import file_
from jeanpaulstart.batch import validator
from jeanpaulstart.constants import *


USER_DATA = {
    'name': 'Task Name',
    'file': {
        'path': 'path',
        'state': 'state'
    }
}


SPLITTED = {
    'name': 'Task Name',
    'command': 'file',
    'arguments': {
        'path': 'path',
        'state': 'state'
    }
}


class MockFileIO(object):
    def mkdir(self, path):
        self.mkdir_called = path

    def remove(self, path):
        self.remove_called = path


class TestTaskCopy(unittest.TestCase):

    def setUp(self):
        self.backup_file_io = file_.file_io
        self.mock_file_io = MockFileIO()
        file_.file_io = self.mock_file_io

    def tearDown(self):
        file_.file_io = self.backup_file_io

    def test_validate(self):
        status, message = file_.validate(USER_DATA)
        self.assertEqual(
            status,
            validator.OK
        )

    def test_normalize(self):
        normalized = file_.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            SPLITTED
        )

    def test_apply_directory(self):
        file_.apply_(path="path", state=STATE_DIRECTORY)

        self.assertEqual(
            self.mock_file_io.mkdir_called,
            "path"
        )

    def test_apply_absent(self):
        file_.apply_(path="path", state=STATE_ABSENT)

        self.assertEqual(
            self.mock_file_io.remove_called,
            "path"
        )
