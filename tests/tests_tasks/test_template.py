import os
import unittest
from copy import deepcopy
from jeanpaulstart.tasks import template
from jeanpaulstart.constants import *


TEMPLATE_CONTENT = """Some template content with a {{ variable }}"""
USER_DATA = {
    'name': 'Task Name',
    'template': {
        'src': 'src',
        'dest': 'dest'
    }
}
SPLITTED = {
    'name': 'Task Name',
    'command': 'template',
    'arguments': {
        'src': 'src',
        'dest': 'dest'
    }
}


class MockJinja(object):
    pass


class MockShutil(object):
    def copyfile(self, src, dest):
        pass


class TestTemplateTask(unittest.TestCase):

    def _backup_environment(self):
        self._environment = dict(os.environ)

    def _restore_environment(self):
        os.environ = dict(self._environment)

    def _mock_jinja(self):
        self._original_jinja = template.jinja2
        self._mocked_jinja = MockJinja()
        template.jinja2 = self._mocked_jinja

    def _restore_jinja(self):
        template.jinja2 = self._original_jinja

    def setUp(self):
        self.user_data = USER_DATA
        self._mock_jinja()
        self._backup_environment()

    def tearDown(self):
        self._restore_jinja()
        self._restore_environment()

    def test_jinja_replace(self):
        self._restore_jinja()

        replaced_content = template._jinja_replace(TEMPLATE_CONTENT, variable="replacement")

        self.assertEqual(
            replaced_content,
            "Some template content with a replacement"
        )

    def test_replace_with_environment(self):
        self._restore_jinja()
        os.environ['variable'] = "replacement from environment"

        replaced_content = template._replace_with_environment(TEMPLATE_CONTENT)

        self.assertEqual(
            replaced_content,
            "Some template content with a replacement from environment"
        )

    def test_validate(self):
        status, message = template.validate(USER_DATA)
        self.assertEqual(
            status,
            OK
        )

    def test_normalize_without_force(self):
        expected = deepcopy(SPLITTED)
        expected['arguments']['force'] = True

        normalized = template.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            expected
        )

    # Todo : Ecrire les tests pour apply_()
