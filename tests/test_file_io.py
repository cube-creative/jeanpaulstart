import os
from jeanpaulstart import file_io
from unittest import TestCase


FILE_ON_DISK = r"""[EXAMPLE]
Something=Some\Value
"""


class MockShutil(object):
    def __init__(self):
        self.copy_called = None, None
        self.rmtree_called = None

    def copy(self, source, destination):
        self.copy_called = source, destination

    def rmtree(self, path):
        self.rmtree_called = path


class MockPath(object):
    isdir_value = False
    isfile_value = True

    def dirname(self, path):
        return os.path.dirname(path)

    def isfile(self, filepath):
        return self.isfile_value

    def isdir(self, dirname):
        return self.isdir_value


class MockOs(object):
    path = MockPath()

    def __init__(self):
        self.makedirs_called = None
        self.unlink_called = None

    def makedirs(self, path):
        self.makedirs_called = path

    def unlink(self, path):
        self.unlink_called = path


class TestFileIO(TestCase):
    FILEPATH = os.path.expandvars("$TEMP/file.j2")

    def setUp(self):
        self.backup_shutil = file_io.shutil
        self.mock_shutil = MockShutil()
        file_io.shutil = self.mock_shutil

        self.backup_os = file_io.os
        self.mock_os = MockOs()
        file_io.os = self.mock_os

        with open(TestFileIO.FILEPATH, 'w+') as template_file:
            template_file.write(FILE_ON_DISK)

    def tearDown(self):
        file_io.os = self.backup_os
        file_io.shutil = self.backup_shutil
        os.remove(TestFileIO.FILEPATH)

    def test_load_template(self):
        template_content = file_io.read_file_utf16(TestFileIO.FILEPATH)

        self.assertEqual(
            template_content,
            FILE_ON_DISK
        )

    def test_copy(self):
        file_io.copy("source", "destination/path/file.extension")

        self.assertEqual(
            ("source", "destination/path/file.extension"),
            self.mock_shutil.copy_called
        )

        self.assertEqual(
            "destination/path",
            self.mock_os.makedirs_called
        )

    def test_copy_not_forced(self):
        file_io.copy("source", "destination", force=False)

        self.assertEqual(
            (None, None),
            self.mock_shutil.copy_called
        )

        self.assertIsNone(
            self.mock_os.makedirs_called
        )

    def test_file_mkdir(self):
        self.mock_os.path.isdir_value = False
        file_io.mkdir("some_path/dir_name")

        self.assertEqual(
            self.mock_os.makedirs_called,
            "some_path/dir_name"
        )

    def test_file_mkdir_already_exists(self):
        self.mock_os.path.isdir_value = True
        file_io.mkdir("some_path/dir_name")

        self.assertIsNone(
            self.mock_os.makedirs_called
        )

    def test_file_remove_file(self):
        self.mock_os.path.isfile_value = True
        file_io.remove("some_path/dir_name/some_file.txt")

        self.assertEqual(
            self.mock_os.unlink_called,
            "some_path/dir_name/some_file.txt"
        )

    def test_file_remove_directory(self):
        self.mock_os.path.isfile_value = False
        self.mock_os.path.isdir_value = True
        file_io.remove("some_path/dir_name")

        self.assertEqual(
            self.mock_shutil.rmtree_called,
            "some_path/dir_name"
        )
