from jeanpaulstart.constants import *


class MockPlugin(object):
    def __init__(self, command_name):
        self.TASK_COMMAND = command_name

    def validate(self, data):
        return OK, ""

    def normalize_after_split(self, data):
        return data

    #TODO : apply_() pour test_executor.py !!
    def apply_(self, *args, **kwargs):
        return TASK_ERROR_IGNORED
