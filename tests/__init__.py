import unittest
from jeanpaulstart import api


BATCH_OK_NORMALIZED_DATA = {}


class Mock(object):

    def install(self):
        pass

    def uninstall(self):
        pass


class Test(unittest.TestCase):

    def setUp(self):
        self.mock = Mock()
        self.mock.install()

    def tearDown(self):
        self.mock.uninstall()

    def test_run_batch(self):
        api.run_batch(BATCH_OK_NORMALIZED_DATA)
