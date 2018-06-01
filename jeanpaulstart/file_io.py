import os
import io
import shutil


def read_file_utf16(filepath):
    try:
        with io.open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with io.open(filepath, 'r', encoding='utf-16') as f:
            return f.read()


def copy(source, destination, force=True):
    if not force and os.path.isfile(destination):
        return

    dirname = os.path.dirname(destination)
    if not os.path.isdir(dirname): os.makedirs(dirname)

    shutil.copy(source, destination)


def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def remove(path):
    if os.path.isfile(path):
        os.unlink(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
