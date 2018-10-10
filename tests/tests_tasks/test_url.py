import unittest
from copy import deepcopy
from jeanpaulstart.tasks import url
from jeanpaulstart.batch import validator


USER_DATA = {
    'name': 'Task Name',
    'url': 'url'
}


SPLITTED = {
    'name': 'Task Name',
    'command': 'url',
    'arguments': 'some://url'
}


class MockWebbrowser(object):
    def open(self, url):
        self.open_called = url


class TestTaskCopy(unittest.TestCase):

    def setUp(self):
        self.backup_webbrowser = url.webbrowser
        self.mock_webbrowser = MockWebbrowser()
        url.webbrowser = self.mock_webbrowser

    def tearDown(self):
        url.webbrowser = self.backup_webbrowser

    def test_validate(self):
        status, message = url.validate(USER_DATA)
        self.assertEqual(
            status,
            validator.OK
        )

    def test_normalize(self):
        expected = deepcopy(SPLITTED)
        expected['arguments'] = {'url': 'some://url'}

        normalized = url.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            expected
        )

    def test_apply_(self):
        url.apply_(url="some://url")

        self.assertEqual(
            self.mock_webbrowser.open_called,
            "some://url"
        )
