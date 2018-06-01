import unittest
from collections import OrderedDict
from jeanpaulstart.constants import *
from jeanpaulstart.batch import normalizer
from mock_data import NORMALIZED_ENV_TASKS
import mock_plugin


def _environment():
    environment = OrderedDict()
    environment['ENV_VAR_1'] = 'value1'
    environment['ENV_VAR_2'] = ['valuea', 'valueb']
    return environment


def _basic_task():
    basic_task = OrderedDict()
    basic_task['name'] = 'Some Name'
    basic_task['command_name'] = {
        'argument1': 'value1',
        'argument2': 'value2'
    }
    basic_task['ignore_errors'] = True
    return basic_task


def _batch_data(environment_present=True):
    data = OrderedDict()
    data['name'] = "Some Name"
    data['icon_path'] = "some/icon/path"
    data['tags'] = ['some', 'tags']
    if environment_present: data['environment'] = _environment()
    data['tasks'] = [
        _basic_task()
    ]
    return data


def _expected_normalized_batch(environment_present=True):
    normalized_batch = OrderedDict()
    normalized_batch['name'] = 'Some Name'
    normalized_batch['icon_path'] = 'some/icon/path'
    normalized_batch['tags'] = ['some', 'tags', TAG_ADMIN]

    normalized_batch['tasks'] = list()

    if environment_present:
        normalized_batch['tasks'] += [
            {
                'name': 'From environment',
                'command': 'environment',
                'ignore_errors': False,
                'register_status': False,
                'arguments':  {'name': 'ENV_VAR_1', 'value': 'value1'}},
            {
                'name': 'From environment',
                'command': 'environment',
                'ignore_errors': False,
                'register_status': False,
                'arguments': {'name': 'ENV_VAR_2', 'value': ['valuea', 'valueb']}}
        ]

    normalized_batch['tasks'] += [
        {
            'name': 'Some Name',
            'command': 'command_name',
            'ignore_errors': True,
            'register_status': False,
            'arguments': {'argument1': 'value1', 'argument2': 'value2'}
        }
    ]
    return normalized_batch


class TestNormalizer(unittest.TestCase):

    def setUp(self):
        self.backup_plugin_module = normalizer.plugin_loader
        self.mock_plugin_module = mock_plugin.MockPluginModule()
        normalizer.plugin_loader = self.mock_plugin_module

    def tearDown(self):
        normalizer.plugin_loader = self.backup_plugin_module

    def test_split_keys(self):
        task = _basic_task()
        splitted = normalizer._split_keys_and_deep_copy(task)

        self.assertEqual(
            splitted,
            {
                'name': 'Some Name',
                'command': 'command_name',
                'arguments': {'argument1': 'value1', 'argument2': 'value2'},
                'ignore_errors': True,
                'register_status': False
            }
        )

    def test_environment(self):
        tasks = normalizer.normalize_environment(_environment())

        self.assertEqual(
            tasks,
            NORMALIZED_ENV_TASKS
        )

    def test_tags_with_duplicate(self):
        tags = normalizer.normalize_tags(['tag1', 'tag1', 'tag2'])

        self.assertEqual(
            tags,
            ['tag1', 'tag1', 'tag2', TAG_ADMIN]
        )

    def test_ignore_errors_missing(self):
        task_dict = {
            'some_command': 'some_arguments'
        }
        ignore_errors = normalizer._ignore_errors(task_dict)

        self.assertFalse(ignore_errors)

    def test_ignore_errors_true(self):
        task_dict = {
            'some_command': 'some_arguments',
            'ignore_errors': True
        }

        ignore_errors = normalizer._ignore_errors(task_dict)

        self.assertTrue(ignore_errors)

    def test_ignore_errors_false(self):
        task_dict = {
            'some_command': 'some_arguments',
            'ignore_errors': False
        }

        ignore_errors = normalizer._ignore_errors(task_dict)

        self.assertFalse(ignore_errors)

    def test_whole_batch(self):
        batch_data = _batch_data()
        normalized = normalizer.normalize_batch(batch_data)

        self.assertDictEqual(
            normalized,
            _expected_normalized_batch()
        )


    def test_whole_batch_no_plugins(self):
        self.mock_plugin_module.loaded_plugins.plugin_missing = True
        batch_data = _batch_data()
        normalized = normalizer.normalize_batch(batch_data)

        self.assertDictEqual(
            normalized,
            _expected_normalized_batch()
        )

    def test_whole_batch_without_environment(self):
        batch_data = _batch_data(environment_present=False)
        normalized = normalizer.normalize_batch(batch_data)

        self.assertDictEqual(
            normalized,
            _expected_normalized_batch(environment_present=False)
        )
