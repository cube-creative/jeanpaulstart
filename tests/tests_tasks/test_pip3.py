import unittest
from copy import deepcopy
from jeanpaulstart.tasks import pip3
from jeanpaulstart.constants import *
from jeanpaulstart.batch import validator


USER_DATA = {
    'name': 'Task Name',
    'pip3': {
        'name': 'git+http://some/repository.git'
    }
}


SPLITTED = {
    'name': 'Task Name',
    'command': 'pip3',
    'arguments': {
        'name': 'git+http://some/repository.git',
        'state': STATE_PRESENT
    }
}


class TestTaskPip(unittest.TestCase):

    def _mock_call(self, command, shell):
        self._mock_call_called = command, shell
        return OK

    def setUp(self):
        self._mock_call_called = None

        self.backup_call = pip3.call
        pip3.call = self._mock_call

    def tearDown(self):
        pip3.call = self.backup_call

    def test_validate(self):
        status, message = pip3.validate(USER_DATA)
        self.assertEqual(
            status,
            validator.OK
        )

    def test_normalize_without_state(self):
        expected = deepcopy(SPLITTED)
        expected['arguments']['state'] = STATE_PRESENT

        normalized = pip3.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            expected
        )

    def test_apply_present(self):
        status = pip3.apply_(name="name.git", state=pip3.STATE_PRESENT)

        self.assertEqual(
            self._mock_call_called,
            ('pip3 install name.git', True)
        )
        self.assertEqual(
            status,
            OK
        )

    def test_apply_force_reinstall(self):
        status = pip3.apply_(name="name.git", state=pip3.STATE_FORCE_REINSTALL)

        self.assertEqual(
            self._mock_call_called,
            ('pip3 install --upgrade name.git', True)
        )
        self.assertEqual(
            status,
            OK
        )
