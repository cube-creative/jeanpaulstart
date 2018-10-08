import os
import jinja2
from jeanpaulstart import file_io
from jeanpaulstart.constants import *


TASK_COMMAND = 'template'


def _jinja_replace(content, **variables):
    template_ = jinja2.Environment(loader=jinja2.BaseLoader).from_string(content)
    return template_.render(**variables)


def _replace_with_environment(content):
    variables = os.environ.copy()
    return _jinja_replace(content, **variables)


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    normalized = dict(splitted)
    normalized['arguments']['force'] = splitted['arguments'].get('force', True)
    return normalized


def apply_(src, dest, force):
    if not force and os.path.isfile(dest):
        return STATE_ALREADY_EXISTS

    dirname = os.path.dirname(dest)
    if not os.path.isdir(dirname): os.makedirs(dirname)

    template_content = file_io.read_file_utf16(src)

    replaced_content = _replace_with_environment(template_content)

    with open(dest, "w+") as dest_file:
        dest_file.write(replaced_content)

    return OK
