import unittest
from copy import deepcopy
from jeanpaulstart.tasks import copy_
from jeanpaulstart.constants import *


USER_DATA = {
    'name': 'Task Name',
    'copy': {
        'src': 'src',
        'dest': 'dest'
    }
}


SPLITTED = {
    'name': 'Task Name',
    'command': 'copy',
    'arguments': {
        'src': 'src',
        'dest': 'dest'
    }
}


class MockFileIO(object):
    def copy(self, src, dest, force):
        self.copy_called = src, dest, force


class TestTaskCopy(unittest.TestCase):

    def setUp(self):
        self.backup_file_io = copy_.file_io
        self.mock_file_io = MockFileIO()
        copy_.file_io = self.mock_file_io

    def tearDown(self):
        copy_.file_io = self.backup_file_io

    def test_validate(self):
        status, message = copy_.validate(USER_DATA)
        self.assertEqual(
            status,
            OK
        )

    def test_normalize_force_absent(self):
        expected = deepcopy(SPLITTED)
        expected['arguments']['force'] = True

        normalized = copy_.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            expected
        )

    def test_normalize_force_present(self):
        expected = deepcopy(SPLITTED)
        expected['arguments']['force'] = False

        splitted = deepcopy(SPLITTED)
        splitted['arguments']['force'] = False

        normalized = copy_.normalize_after_split(splitted)

        self.assertDictEqual(
            normalized,
            expected
        )

    def test_apply_(self):
        status = copy_.apply_(src="src", dest="dest", force="force")

        self.assertEqual(
            self.mock_file_io.copy_called,
            ("src", "dest", "force")
        )
        self.assertEqual(
            status,
            OK
        )
