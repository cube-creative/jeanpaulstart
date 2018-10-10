import unittest
from copy import deepcopy
from jeanpaulstart.constants import *
from jeanpaulstart.tasks import environment


USER_DATA = {
    'name': 'Task Name',
    'environment': {
        'name': 'name',
        'value': 'value'
    }
}


SPLITTED = {
    'name': 'Task Name',
    'command': 'environment',
    'arguments': {
        'name': 'name',
        'value': 'value'
    }
}


class MockEnvironment(object):
    def set(self, name, value):
        self.set_env_variable_called = name, value


class TestTaskEnvironment(unittest.TestCase):

    def setUp(self):
        self.backup_environment = environment.environment
        self.mock_environment = MockEnvironment()
        environment.environment = self.mock_environment

    def tearDown(self):
        environment.environment= self.backup_environment

    def test_validate(self):
        status, message = environment.validate(USER_DATA)
        self.assertEqual(
            status,
            OK
        )

    def test_normalize(self):
        normalized = environment.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            SPLITTED
        )

    def test_apply_(self):
        status = environment.apply_(name="name", value="value")

        self.assertEqual(
            self.mock_environment.set_env_variable_called,
            ("name", "value")
        )
        self.assertEqual(
            status,
            OK
        )
