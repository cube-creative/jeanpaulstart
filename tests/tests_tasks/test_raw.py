import unittest
from copy import deepcopy
from jeanpaulstart.tasks import raw
from jeanpaulstart.constants import *


USER_DATA = {
    'name': 'Task Name',
    'raw': {
        'command': 'command'
    }
}


SPLITTED = {
    'name': 'Task Name',
    'command': 'raw',
    'arguments': {
        'command': 'command'
    }
}


class TestTaskRaw(unittest.TestCase):

    def _mock_popen(self, command, shell, close_fds):
        self._mock_popen_called = command, shell, close_fds

    def _mock_call(self, command, shell):
        self._mock_call_called = command, shell

    def setUp(self):
        self._mock_popen_called = None
        self._mock_call_called = None

        self.backup_popen = raw.Popen
        self.backup_call = raw.call
        raw.Popen= self._mock_popen
        raw.call = self._mock_call

    def tearDown(self):
        raw.Popen= self.backup_popen
        raw.call = self.backup_call

    def test_validate(self):
        status, message = raw.validate(USER_DATA)
        self.assertEqual(
            status,
            OK
        )

    def test_normalize_without_async(self):
        expected = deepcopy(SPLITTED)
        expected['arguments']['async'] = True

        normalized = raw.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            expected
        )

    def test_apply_not_async(self):
        raw.apply_(async=False, command="command")

        self.assertEqual(
            self._mock_call_called,
            ('command', True)
        )

        self.assertIsNone(self._mock_popen_called)

    def test_apply_async(self):
        raw.apply_(async=True, command="command")

        self.assertEqual(
            self._mock_popen_called,
            ('command', True, True)
        )

        self.assertIsNone(self._mock_call_called)
