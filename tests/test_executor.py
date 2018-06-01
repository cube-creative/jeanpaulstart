import unittest
from jeanpaulstart import executor
from jeanpaulstart.constants import *
import mock_plugin
from mock_data import _batch


class TestExecutor(unittest.TestCase):

    def setUp(self):
        self.backup_plugin_module = executor.plugin_loader
        self.mock_plugin_module = mock_plugin.MockPluginModule()
        executor.plugin_loader = self.mock_plugin_module

    def tearDown(self):
        executor.plugin_loader = self.backup_plugin_module

    def test_run_batch(self):
        status = executor.run_batch(_batch('Some Batch'))

        self.assertEqual(
            status,
            OK
        )

        # TODO : euh ? il manque rien la ?
        # Il manque de checker que l'environment soit le meme avant et apres

    def test_run_batch_register_status(self):
        status = executor.run_batch(_batch('Some Batch', register_status_for_raw=True))

        self.assertEqual(
            status,
            ERROR_IGNORED
        )
