import os
import unittest
from glob import glob
from jeanpaulstart import plugin_loader
import mock_plugin


PLUGIN_1_CONTENT = """
def ca():
    return 4
"""  # Basic content to test loader


class TestPluginLoader(unittest.TestCase):

    def _mock_load(self, plugin_name=None, plugin_filepath=None):
        return self._mock_plugins[plugin_name]

    def _mock_validate(self, plugin):
        if self._mock_plugins_valid:
            return plugin_loader.Loader.OK
        else:
            return plugin_loader.Loader.VALIDATE_MISSING

    def setUp(self):
        self.plugin_folder = os.path.join(os.path.dirname(__file__), "plugins")

        self._mock_plugins_valid = True

        self._mock_plugins = {
            'plugin_1': mock_plugin.MockPlugin("plugin_1"),
            'plugin_2': mock_plugin.MockPlugin("plugin_2")
        }

        self.temp_plugin_folder = os.path.expandvars("$TEMP/jeanpaulstart/plugins")
        self.plugin_1_filepath = os.path.expandvars("$TEMP/jeanpaulstart/plugins/plugin_1.py")
        self.plugin_2_filepath = os.path.expandvars("$TEMP/jeanpaulstart/plugins/plugin_2.py")

        if not os.path.isdir(self.temp_plugin_folder):
            os.makedirs(self.temp_plugin_folder)

        if os.path.isfile(self.plugin_1_filepath):
            os.remove(self.plugin_1_filepath)

        with open(self.plugin_1_filepath, "w+") as f_plugin_1:
            f_plugin_1.write(PLUGIN_1_CONTENT)

        if os.path.isfile(self.plugin_2_filepath):
            os.remove(self.plugin_2_filepath)

        with open(self.plugin_2_filepath, "w+"):
            pass

        self.loader = plugin_loader.Loader(plugin_folder=self.temp_plugin_folder)

    def tearDown(self):
        for filepath in glob(self.temp_plugin_folder + "/*.*"):
            os.remove(filepath)

        if os.path.isdir(self.temp_plugin_folder):
            os.rmdir(self.temp_plugin_folder)

    def test_list_plugin_names(self):
        plugins = self.loader.list_names()

        self.assertEqual(
            plugins,
            ["plugin_1", "plugin_2"]
        )

    def test_make_plugin_filepath(self):
        self.loader.plugin_folder = "/plugin/folder"
        plugin_filepath = self.loader.make_plugin_filepath(plugin_name="plugin_1")

        self.assertEqual(
            plugin_filepath,
            "/plugin/folder/plugin_1.py"
        )

    def test_load_by_name(self):
        plugin = self.loader.load(plugin_name="plugin_1")

        self.assertTrue(hasattr(
            plugin,
            "ca"
        ))

    def test_load_by_filepath(self):
        filepath = os.path.join(self.plugin_folder, "plugin-ok.py")
        plugin = self.loader.load(plugin_filepath=filepath)

        self.assertTrue(hasattr(
            plugin,
            "validate"
        ))

    def test_load_by_filepath_missing(self):
        filepath = os.path.join(os.path.dirname(__file__), "plugin-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)

        self.assertIsNone(plugin)

    def test_load_erroneous(self):
        with open(self.plugin_1_filepath, "w+") as f_plugin_1:
            f_plugin_1.write("wrong python data")

        self.assertRaises(
            SyntaxError,
            self.loader.load,
            plugin_name="plugin_1"
        )

    def test_validate_ok(self):
        filepath = os.path.join(self.plugin_folder, "plugin-ok.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            plugin_loader.Loader.OK
        )

    def test_validate_task_command_missing(self):
        filepath = os.path.join(os.path.dirname(__file__), "plugin-task-command-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            plugin_loader.Loader.TASK_COMMAND_MISSING
        )

    def test_validate_task_command_not_str(self):
        filepath = os.path.join(self.plugin_folder, "plugin-task-command-not-str.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            plugin_loader.Loader.TASK_COMMAND_NOT_STR
        )

    def test_validate_missing(self):
        filepath = os.path.join(self.plugin_folder, "plugin-validate-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            plugin_loader.Loader.VALIDATE_MISSING
        )

    def test_normalize_missing(self):
        filepath = os.path.join(self.plugin_folder, "plugin-normalize-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            plugin_loader.Loader.NORMALIZE_MISSING
        )

    def test_apply_missing(self):
        filepath = os.path.join(self.plugin_folder, "plugin-apply-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            plugin_loader.Loader.APPLY_MISSING
        )

    def test_load_all(self):
        self.loader.load = self._mock_load
        self.loader.validate = self._mock_validate
        plugin_1 = self._mock_plugins['plugin_1']
        plugin_2 = self._mock_plugins['plugin_2']

        plugins = self.loader.load_all()

        self.assertDictEqual(
            plugins,
            {
                "plugin_1": plugin_1,
                "plugin_2": plugin_2
            }
        )

    def load_all_invalid_plugins(self):
        self._mock_plugins_valid = False
        self.loader.load = self._mock_load
        self.loader.validate = self._mock_validate

        plugins = self.loader.load_all()

        self.assertDictEqual(
            plugins,
            {}
        )

    def test_init(self):
        has_loaded = plugin_loader.init(self.plugin_folder, force=True)
        self.assertEqual(
            len(plugin_loader.loaded_plugins),
            1
        )

        self.assertEqual(
            plugin_loader.loaded_plugins.keys(),
            ['command-name']
        )

        self.assertTrue(has_loaded)

    def test_init_twice(self):
        plugin_loader.init(self.plugin_folder)
        has_loaded = plugin_loader.init(self.plugin_folder)

        self.assertFalse(has_loaded)

    def test_init_twice_with_force(self):
        plugin_loader.init(self.plugin_folder)
        has_loaded = plugin_loader.init(self.plugin_folder, force=True)

        self.assertTrue(has_loaded)

    def test_load_already_loaded(self):
        pass
