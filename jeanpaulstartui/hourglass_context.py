

class HourglassContext(object):
    def __init__(self, view):
        self._view = view

    def __enter__(self):
        self._view.set_hourglass(True)
        return self

    def __exit__(self, type, value, traceback):
        self._view.set_hourglass(False)
