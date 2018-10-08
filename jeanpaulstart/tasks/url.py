import webbrowser
from jeanpaulstart.constants import *


TASK_COMMAND = 'url'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    splitted['arguments'] = {'url': splitted['arguments']}
    return splitted


def apply_(url):
    webbrowser.open(url)
    return OK
