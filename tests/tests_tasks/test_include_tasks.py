import os
import unittest
from jeanpaulstart.tasks import include_tasks
from jeanpaulstart.constants import *
from tests.mock_data import BATCH_YAML_CONTENT


USER_DATA = {
    'name': 'Task Name',
    'copy': {
        'src': 'src',
        'dest': 'dest'
    }
}


class MockAPI(object):
    def __init__(self):
        self.run_from_filepath_called = None

    def run_from_filepath(self, filepath):
        self.run_from_filepath_called = filepath
        return OK


class TestTaskIncludeTasks(unittest.TestCase):

    def setUp(self):
        self.mock_api = MockAPI()
        self.backup_run_from_filepath = include_tasks.jeanpaulstart.run_from_filepath
        include_tasks.jeanpaulstart.run_from_filepath = self.mock_api.run_from_filepath

        self.yaml_filepath = os.path.expandvars("$TEMP/jeanpaulstart/batch1.yml").replace('\\', '/')

        if os.path.isfile(self.yaml_filepath):
            os.remove(self.yaml_filepath)

        with open(self.yaml_filepath, "w+") as f_yaml:
            f_yaml.write(BATCH_YAML_CONTENT)

    def tearDown(self):
        include_tasks.jeanpaulstart.run_from_filepath = self.backup_run_from_filepath

        if os.path.isfile(self.yaml_filepath):
            os.remove(self.yaml_filepath)

    def test_validate(self):
        status, message = include_tasks.validate(USER_DATA)
        self.assertEqual(
            status,
            OK
        )

    def test_apply_(self):
        status = include_tasks.apply_(file=self.yaml_filepath)

        self.assertEqual(
            self.mock_api.run_from_filepath_called,
            self.yaml_filepath
        )
        self.assertEqual(
            status,
            OK
        )
