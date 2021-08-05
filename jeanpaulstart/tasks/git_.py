import git
import os
from jeanpaulstart.constants import *

TASK_COMMAND = 'git'
DEFAULT_BRANCH = 'master'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    splitted['arguments']['branch'] = splitted['arguments'].get('branch', DEFAULT_BRANCH)
    return splitted


def apply_(url, dest, branch):
    checkout_remote(url, dest, branch)

    return OK


def checkout_remote(url, dest, branch):
    if not os.path.exists(dest):
        repo = git.Repo.clone_from(url, dest)
    else:
        repo = git.Repo(dest)

    repo.git.reset("--hard")
    repo.git.clean("-dfx")
    repo.git.pull("origin", branch)
    repo.git.checkout(branch)
