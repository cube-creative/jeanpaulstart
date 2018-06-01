from jeanpaulstart import constants


class MockPlugin(object):
    def __init__(self, command_name):
        self.TASK_COMMAND = command_name

    def validate(self, data):
        return constants.OK, ""

    def normalize_after_split(self, data):
        return data

    #TODO : apply_() pour test_executor.py !!
    def apply_(self, *args, **kwargs):
        return constants.ERROR_IGNORED


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
