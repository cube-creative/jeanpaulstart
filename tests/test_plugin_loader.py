import os
import unittest
from glob import glob
from jeanpaulstart import constants, plugin_loader
from mock_plugin import MockPlugin


PLUGIN_1_CONTENT = """
def ca():
    return 4
"""  # Basic content to test loader


class MockLoadedPlugins(object):
    def __init__(self):
        self.plugin_missing = False

    def get(self, name, default):
        if self.plugin_missing:
            return default

        return MockPlugin('command_name')

    def keys(self):
        if self.plugin_missing:
            return []

        return ['command_name']

    def __getitem__(self, item):
        if not self.plugin_missing:
            return MockPlugin('command_name')


class MockPluginModule(object):
    def __init__(self):
        self.loaded_plugins = MockLoadedPlugins()


class TestPluginLoader(unittest.TestCase):

    def _mock_load(self, plugin_name=None, plugin_filepath=None):
        return self._mock_plugins[plugin_name]

    def _mock_validate(self, plugin):
        if self._mock_plugins_valid:
            return constants.OK
        else:
            return constants.PLUG_VALIDATE_MISSING

    def setUp(self):
        self.plugin_folder = os.path.join(os.path.dirname(__file__), "plugins")

        self._mock_plugins_valid = True

        self._mock_plugins = {
            'plugin_1': MockPlugin("plugin_1"),
            'plugin_2': MockPlugin("plugin_2")
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

    def test_repr(self):
        repr = str(self.loader)
        expected_repr = "Loader(folder={})".format(self.temp_plugin_folder)

        self.assertEqual(
            repr,
            expected_repr
        )

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
            constants.OK
        )

    def test_validate_task_command_missing(self):
        filepath = os.path.join(os.path.dirname(__file__), "plugin-task-command-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            constants.PLUG_COMMAND_MISSING
        )

    def test_validate_task_command_not_str(self):
        filepath = os.path.join(self.plugin_folder, "plugin-task-command-not-str.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            constants.PLUG_COMMAND_NOT_STR
        )

    def test_validate_missing(self):
        filepath = os.path.join(self.plugin_folder, "plugin-validate-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            constants.PLUG_VALIDATE_MISSING
        )

    def test_normalize_missing(self):
        filepath = os.path.join(self.plugin_folder, "plugin-normalize-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            constants.PLUG_NORMALIZE_MISSING
        )

    def test_apply_missing(self):
        filepath = os.path.join(self.plugin_folder, "plugin-apply-missing.py")
        plugin = self.loader.load(plugin_filepath=filepath)
        status = self.loader.validate(plugin)

        self.assertEqual(
            status,
            constants.PLUG_APPLY_MISSING
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
