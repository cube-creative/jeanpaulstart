from jeanpaulstart.constants import *


TASK_COMMAND = 'line_in_file'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    splitted['arguments']['replace'] = splitted['arguments'].get('replace', False)
    return splitted


def apply_(filepath, value, insert_after, replace):
    print(filepath, value, insert_after, replace)
    insert_line(filepath, value, insert_after, replace)

    return OK


def insert_line(filepath, value, insert_after, replace):
    value += "\n"
    with open(filepath) as f:
        content = f.readlines()

    row = 0
    if insert_after:
        for index, line in enumerate(content):
            if line.strip() == insert_after:
                row = index + 1
                break

    if content[row] == value and not replace:
        return

    content.insert(row, value)

    with open(filepath, 'w') as f:
        for line in content:
            f.write(line)
