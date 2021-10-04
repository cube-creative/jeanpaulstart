import os
import shutil
from jeanpaulstart.constants import *


TASK_COMMAND = 'delete'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    return splitted


def apply_(path):
    if not os.path.exists(path):
        return OK

    if os.path.isdir(path):
        if path[-1] in ("/", "\\"):  # Delete content
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)

                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.system('rmdir /S /Q "{}"'.format(file_path))
                    # shutil.rmtree(file_path)
        else:  # Delete whole directory
            os.system('rmdir /S /Q "{}"'.format(path))
            # shutil.rmtree(path)
    else:
        os.remove(path)

    return OK
