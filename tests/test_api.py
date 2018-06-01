import os
import unittest
from glob import glob
from collections import OrderedDict
from jeanpaulstart import api
from jeanpaulstart import tasks
from jeanpaulstart import plugin_loader
from jeanpaulstart.constants import *
from mock_data import \
    BATCH_YAML_CONTENT, \
    BATCH_JSON_CONTENT, \
    BATCH_JSON_CONTENT_NORMALIZED,\
    BATCH_JSON_CONTENT_NOT_VALID, \
    TAGS_FILE_CONTENT, \
    DUMPED_NORMALIZED, \
    DUMPED_NOT_NORMALIZED, \
    _expected_batches, \
    _batch_not_normalized, \
    _batch


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.plugin_path = os.path.dirname(tasks.__file__)
        self._mock_batch_run = None
        self.batch_folder = os.path.expandvars("$TEMP/jeanpaulstart")
        self.yaml_filepath = os.path.expandvars("$TEMP/jeanpaulstart/batch1.yml").replace('\\', '/')
        self.json_filepath = os.path.expandvars("$TEMP/jeanpaulstart/batch2.json").replace('\\', '/')
        self.tags_filepath = os.path.expandvars("$TEMP/jeanpaulstart/tags.yml").replace('\\', '/')

        if os.path.isfile(self.yaml_filepath):
            os.remove(self.yaml_filepath)

        if os.path.isfile(self.json_filepath):
            os.remove(self.json_filepath)

        if os.path.isfile(self.tags_filepath):
            os.remove(self.tags_filepath)

        if os.path.isdir(self.batch_folder):
            os.rmdir(self.batch_folder)

        os.makedirs(self.batch_folder)

        with open(self.yaml_filepath, "w+") as f_yaml:
            f_yaml.write(BATCH_YAML_CONTENT)

        with open(self.json_filepath, "w+") as f_json:
            f_json.write(BATCH_JSON_CONTENT)

        with open(self.tags_filepath, "w+") as f_tags:
            f_tags.write(TAGS_FILE_CONTENT)

        plugin_loader.init(force=True)

    def tearDown(self):
        if os.path.isfile(self.yaml_filepath):
            os.remove(self.yaml_filepath)

        if os.path.isfile(self.json_filepath):
            os.remove(self.json_filepath)

        if os.path.isfile(self.tags_filepath):
            os.remove(self.tags_filepath)

        if os.path.isdir(self.batch_folder):
            os.rmdir(self.batch_folder)

        plugin_loader.init(
            plugin_folder="impossible/folder",
            force=True
        )

    def _mock_run(self, batch):
        self._mock_batch_run = batch

    def test_batches_from_folder(self):
        batches = api.batches_from_folders([self.batch_folder])

        self.assertEqual(
            batches,
            _expected_batches()
        )

    def test_batches_for_user(self):
        batches = api.batches_for_user(
            batch_directories=[self.batch_folder],
            tags_filepath=self.tags_filepath,
            username="t.est"
        )

        self.assertEqual(
            batches,
            [_batch('Yaml Name')]
        )

    def test_run_batch(self):
        batch = _batch("Some Name")
        executor_run_backup = api.executor.run_batch
        api.executor.run_batch = self._mock_run

        api.run_batch(batch)

        api.executor.run_batch = executor_run_backup

        self.assertEqual(
            self._mock_batch_run,
            batch
        )

    def test_run_from_json(self):
        executor_run_backup = api.executor.run_batch
        api.executor.run_batch = self._mock_run

        api.run_from_json(BATCH_JSON_CONTENT_NORMALIZED)

        api.executor.run_batch = executor_run_backup

        self.assertEqual(
            self._mock_batch_run,
            _batch("JSON Name", tags_3_4=True)
        )

    def test_run_from_json_not_valid(self):
        executor_run_backup = api.executor.run_batch
        api.executor.run_batch = self._mock_run

        status = api.run_from_json(BATCH_JSON_CONTENT_NOT_VALID, normalized=False)

        api.executor.run_batch = executor_run_backup

        self.assertEqual(
            self._mock_batch_run,
            None
        )

        self.assertEqual(
            status,
            NAME_MISSING
        )

    def test_run_from_json_without_normalization(self):
        executor_run_backup = api.executor.run_batch
        api.executor.run_batch = self._mock_run

        api.run_from_json(BATCH_JSON_CONTENT, normalized=False)

        api.executor.run_batch = executor_run_backup

        self.assertEqual(
            self._mock_batch_run,
            _batch("JSON Name", tags_3_4=True)
        )

    def test_dump_data_for_command_line(self):
        data = _batch_not_normalized("JSON Name", tags_3_4=True)
        dumped = api.dump_data_for_command_line(data)

        self.assertItemsEqual(
            dumped,
            DUMPED_NORMALIZED
        )

    def test_dump_data_for_command_line_without_normalization(self):
        data = _batch_not_normalized("JSON Name", tags_3_4=True)
        dumped = api.dump_data_for_command_line(data, normalize=False)

        self.assertItemsEqual(
            dumped,
            DUMPED_NOT_NORMALIZED
        )

    def test_dump_data_for_command_line_not_valid(self):
        data = _batch_not_normalized("JSON Name", tags_3_4=True)
        data.pop('name')
        dumped = api.dump_data_for_command_line(data)

        self.assertEqual(
            dumped,
            None
        )

    def test_dump_file_for_command_line(self):
        dumped = api.dump_file_for_command_line(self.json_filepath)

        self.assertEqual(
            dumped,
            DUMPED_NORMALIZED
        )

    def test_dump_file_for_command_line_without_normalization(self):
        dumped = api.dump_file_for_command_line(self.json_filepath, normalize=False)

        self.assertEqual(
            dumped,
            DUMPED_NOT_NORMALIZED
        )

    def test_run_from_filepath_yaml(self):
        executor_run_backup = api.executor.run_batch
        api.executor.run_batch = self._mock_run

        api.run_from_filepath(self.yaml_filepath)

        self.assertEqual(
            OrderedDict([
                ('name', 'Yaml Name'),
                ('icon_path', 'some/icon/path'),
                ('tags', ['tag1', 'tag2', 'admin']),
                ('tasks',
                    [{
                        'ignore_errors': False,
                        'register_status': False,
                        'command': 'environment',
                        'name': 'From environment',
                        'arguments': {'name': 'ENV_VAR1', 'value': 'value1'}},
                    {
                        'ignore_errors': False,
                        'register_status': False,
                        'command': 'environment',
                        'name': 'From environment',
                        'arguments': {'name': 'ENV_VAR2', 'value': ['valuea', 'valueb']}},
                    {
                        'ignore_errors': False,
                        'register_status': False,
                        'command': 'raw',
                        'name': 'Some Task',
                        'arguments': OrderedDict([('command', 'some command'), ('async', False)])}]
                )
            ]),
            self._mock_batch_run
        )

        api.executor.run_batch = executor_run_backup

    def test_run_from_filepath_json(self):
        executor_run_backup = api.executor.run_batch
        api.executor.run_batch = self._mock_run

        api.run_from_filepath(self.json_filepath)

        self.assertEqual(
            OrderedDict([
                ('name', 'JSON Name'),
                ('icon_path', 'some/icon/path'),
                ('tags', ['tag3', 'tag4', 'admin']),
                ('tasks',
                    [{
                        'ignore_errors': False,
                        'register_status': False,
                        'command': 'environment',
                        'name': 'From environment',
                        'arguments': {'name': 'ENV_VAR1', 'value': 'value1'}},
                    {
                        'ignore_errors': False,
                        'register_status': False,
                        'command': 'environment',
                        'name': 'From environment',
                        'arguments': {'name': 'ENV_VAR2', 'value': ['valuea', 'valueb']}},
                    {
                        'ignore_errors': False,
                        'register_status': False,
                        'command': 'raw',
                        'name': 'Some Task',
                        'arguments': OrderedDict([('command', 'some command'), ('async', False)])}]
                )
            ]),
            self._mock_batch_run
        )

        api.executor.run_batch = executor_run_backup

    def test_run_from_filepath_missing(self):
        self.assertIsNone(
            api.run_from_filepath("invalid/batch")
        )

    def test_run_from_filepath_invalid(self):
        self.assertIsNone(
            api.run_from_filepath(self.tags_filepath)
        )

    def test_load_plugins(self):
        api.load_plugins()
        plugin_files = glob(os.path.join(self.plugin_path, "*.py"))

        self.assertEqual(
            len(plugin_loader.loaded_plugins),
            len(plugin_files) - 1
        )


# TODO : Tests for new functions
