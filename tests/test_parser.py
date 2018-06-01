import os
import unittest
from collections import OrderedDict
from jeanpaulstart.batch import parser


YAML_TEXT = r"""---
key1: value1
key2: 2
key3:
    - true
    - false
..."""


JSON_TEXT = r"""{
    "key1": "value1",
    "key2": 2,
    "key3": [true, false]
}"""


def _make_expected_data():
    expected_data = OrderedDict()
    expected_data['key1'] = 'value1'
    expected_data['key2'] = 2
    expected_data['key3'] = [True, False]

    return expected_data


class TestParser(unittest.TestCase):

    def setUp(self):
        self.expected_data = _make_expected_data()
        self.folder = os.path.expandvars("$TEMP/jeanpaulstart")
        self.yaml_filepath = os.path.expandvars("$TEMP/jeanpaulstart/content1.yml").replace('\\', '/')
        self.json_filepath = os.path.expandvars("$TEMP/jeanpaulstart/content2.json").replace('\\', '/')

        if os.path.isfile(self.yaml_filepath):
            os.remove(self.yaml_filepath)

        if os.path.isfile(self.json_filepath):
            os.remove(self.json_filepath)

        if os.path.isdir(self.folder):
            os.rmdir(self.folder)

        os.makedirs(self.folder)

        with open(self.yaml_filepath, "w+") as f_yaml:
            f_yaml.write(YAML_TEXT)

        with open(self.json_filepath, "w+") as f_json:
            f_json.write(JSON_TEXT)

    def tearDown(self):
        if os.path.isfile(self.yaml_filepath):
            os.remove(self.yaml_filepath)

        if os.path.isfile(self.json_filepath):
            os.remove(self.json_filepath)

        if os.path.isdir(self.folder):
            os.rmdir(self.folder)

    def test_from_yaml_content(self):
        data = parser.from_yaml(YAML_TEXT)

        self.assertEqual(
            data,
            self.expected_data
        )

    def test_from_json_content(self):
        data = parser.from_json(JSON_TEXT)

        self.assertEqual(
            data,
            self.expected_data
        )

    def test_from_yaml_file(self):
        data = parser._from_yaml_file(self.yaml_filepath)

        self.assertEqual(
            data,
            self.expected_data
        )

    def test_from_json_file(self):
        data = parser._from_json_file(self.json_filepath)

        self.assertEqual(
            data,
            self.expected_data
        )

    def test_from_folder(self):
        data = parser.from_folders([self.folder])

        self.assertEqual(
            data,
            [
                (self.yaml_filepath, self.expected_data),
                (self.json_filepath, self.expected_data)
            ]
        )
