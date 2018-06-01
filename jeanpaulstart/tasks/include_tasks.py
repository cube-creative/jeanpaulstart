import jeanpaulstart


TASK_COMMAND = 'include_tasks'


def validate(user_data):
    return jeanpaulstart.OK, ""


def normalize_after_split(splitted):
    return splitted


def apply_(file):
    jeanpaulstart.run_from_filepath(file)
