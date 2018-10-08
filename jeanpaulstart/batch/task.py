

class Task(object):
    """
    Object holding infos for a Task (batch step)
    """
    def __init__(self, name, command_name, arguments):
        self.name = name
        self.command_name = command_name
        self.arguments = arguments
        self.ignore_errors = False
        self.register_status = False
        self.abort_on_failure = True
