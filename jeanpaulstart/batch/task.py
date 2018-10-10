

class Task(object):
    """
    Object holding infos for a Task (batch step)
    """
    def __init__(self, name, command_name, arguments):
        self.name = name
        self.command_name = command_name
        self.arguments = arguments
        self.catch_exception = False
        self.exit_if_not_ok = True
        self.register_status = False
        self.when = "True"

    def __repr__(self):
        return "Task(name='{name}', command_name={command}, when={when})".format(
            name=self.name,
            command=self.command_name,
            when=self.when
        )
