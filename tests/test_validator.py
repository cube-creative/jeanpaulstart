import unittest
from collections import OrderedDict
from jeanpaulstart.batch import validator
import mock_plugin


def _make_data_ok():
    environment = OrderedDict()
    environment['ENV_VAR_1'] = 'env_var_1'
    environment['ENV_VAR_2'] = 'env_var_2'

    data = OrderedDict()
    data['name'] = 'a name'
    data['icon_path'] = 'path/to/icon'
    data['tags'] = ['tag1', 'tag2']
    data['environment'] = environment
    data['tasks'] = [
        OrderedDict([
            ('name', 'task1'),
            ('command', 'arguments1')
        ]),
        OrderedDict([
            ('name', 'task2'),
            ('command', 'arguments2')
        ])
    ]

    return data


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.backup_plugin_module = validator.plugin_loader
        self.mock_plugin_module = mock_plugin.MockPluginModule()
        validator.plugin_loader = self.mock_plugin_module

    def tearDown(self):
        validator.plugin_loader = self.backup_plugin_module

    def test_ok(self):
        data = _make_data_ok()
        status, message = validator.validate(data)

        self.assertEqual(status, validator.OK)

    def test_ok_without_environement(self):
        data = _make_data_ok()
        data.pop('environment')
        status, message = validator.validate(data)

        self.assertEqual(status, validator.OK)

    def test_name_missing(self):
        data = _make_data_ok()
        data.pop('name')
        status, message = validator.validate(data)

        self.assertEqual(status, validator.NAME_MISSING)

    def test_name_not_string(self):
        data = _make_data_ok()
        data['name'] = 5
        status, message = validator.validate(data)

        self.assertEqual(status, validator.NAME_NOT_STRING)

    def test_icon_missing(self):
        data = _make_data_ok()
        data.pop('icon_path')
        status, message = validator.validate(data)

        self.assertEqual(status, validator.ICON_MISSING)

    def test_tags_missing(self):
        data = _make_data_ok()
        data.pop('tags')
        status, message = validator.validate(data)

        self.assertEqual(status, validator.TAGS_MISSING)

    def test_tags_not_list(self):
        data = _make_data_ok()
        data['tags'] = {'tag1': 'tag2'}
        status, message = validator.validate(data)

        self.assertEqual(status, validator.TAGS_NOT_LIST)

    def test_tasks_missing(self):
        data = _make_data_ok()
        data.pop('tasks')
        status, message = validator.validate(data)

        self.assertEqual(status, validator.TASKS_MISSING)
        self.assertEqual(message, "")

    def test_tasks_not_list(self):
        data = _make_data_ok()
        data['tasks'] = {'task1': 'command'}
        status, message = validator.validate(data)

        self.assertEqual(status, validator.TASKS_NOT_LIST)

    def test_task_plugin_not_found(self):
        self.mock_plugin_module.loaded_plugins.plugin_missing = True
        data = _make_data_ok()
        status, message = validator.validate(data)

        self.assertEqual(status, validator.TASK_PLUGIN_NOT_FOUND)
