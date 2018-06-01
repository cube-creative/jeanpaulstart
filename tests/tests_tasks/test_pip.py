import unittest
from copy import deepcopy
from jeanpaulstart.tasks import pip
from jeanpaulstart.constants import STATE_PRESENT
from jeanpaulstart.batch import validator


USER_DATA = {
    'name': 'Task Name',
    'pip': {
        'name': 'git+http://some/repository.git'
    }
}


SPLITTED = {
    'name': 'Task Name',
    'command': 'pip',
    'arguments': {
        'name': 'git+http://some/repository.git',
        'state': STATE_PRESENT
    }
}


class TestTaskPip(unittest.TestCase):

    def _mock_call(self, command, shell):
        self._mock_call_called = command, shell

    def setUp(self):
        self._mock_call_called = None

        self.backup_call = pip.call
        pip.call = self._mock_call

    def tearDown(self):
        pip.call = self.backup_call

    def test_validate(self):
        status, message = pip.validate(USER_DATA)
        self.assertEqual(
            status,
            validator.OK
        )

    def test_normalize_without_state(self):
        expected = deepcopy(SPLITTED)
        expected['arguments']['state'] = STATE_PRESENT

        normalized = pip.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            expected
        )

    def test_apply_present(self):
        pip.apply_(name="name.git", state=pip.STATE_PRESENT)

        self.assertEqual(
            self._mock_call_called,
            ('pip install name.git', True)
        )

    def test_apply_force_reinstall(self):
        pip.apply_(name="name.git", state=pip.STATE_FORCE_REINSTALL)

        self.assertEqual(
            self._mock_call_called,
            ('pip install --upgrade name.git', True)
        )
