from jeanpaulstart.constants import *


TASK_COMMAND = 'line_in_file'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    splitted['arguments']['replace'] = splitted['arguments'].get('replace', False)
    return splitted


def apply_(filepath, value, insert_after, replace):
    insert_line(filepath, value, insert_after, replace)

    return OK


def insert_line(filepath, value, insert_after, replace):
    value += "\n"
    with open(filepath) as f:
        content = f.readlines()

    if insert_after:
        row = None
        for index, line in enumerate(content):
            if line == insert_after + '\n':
                row = index + 1
                break
    else:
        row = 0

    if content[row] == value and not replace:
        return

    if row is not None:
        content.insert(row, value)

    with open(filepath, 'w') as f:
        for line in content:
            f.write(line)
