import os
import io
import shutil
import distutils.dir_util


def read_file_utf16(filepath):
    try:
        with io.open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with io.open(filepath, 'r', encoding='utf-16') as f:
            return f.read()


def copy(source, destination, force=True, replace=False):
    if not force and os.path.exists(destination):
        return

    # If source is a directory, this must be a directory too and
    # if the destination exists, is a file, an exception is raised.
    if os.path.isdir(source) and os.path.isfile(destination):
        raise ValueError('The destination must be a directory')

    # If destination is a non-existent path and if either destination ends
    # with "/" or source is a directory, destination is created.
    if not os.path.exists(destination):
        if destination.endswith('/') or os.path.isdir(source):
            os.makedirs(destination)

    # If the source is a file and the destination dirname is a non-existent
    # path, dirname is created.
    if os.path.isfile(source):
        dirname = os.path.dirname(destination)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    if os.path.isdir(source) and os.path.isdir(destination):
        if not destination.endswith('/'):
            name = os.path.split(source)[-1]
            destination = os.path.join(destination, name)

        # Clear
        if replace:
            shutil.rmtree(destination)

        distutils.dir_util.copy_tree(source, destination)
        # shutil.copytree(source, destination, dirs_exist_ok=True)
        # dirs_exist_ok only introduced in 3.8

    else:
        shutil.copy(source, destination)


def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def remove(path):
    if os.path.isfile(path):
        os.unlink(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
