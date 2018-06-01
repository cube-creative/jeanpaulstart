import re
import jeanpaulstart
from jeanpaulstartui.hourglass_context import HourglassContext
from jeanpaulstartui.view.launcher_widget import LauncherWidget


REGEX = re.compile(r'\[([^\]]+)\]')


def _parse_message(message):  # Un peu vilain
    matches = REGEX.findall(message)
    if matches:
        return matches[0] + " : " + matches[1]


class Launcher(object):

    def __init__(self):
        self._view = LauncherWidget()
        self._view.controller = self
        self.batch_directories = list()
        self.tags_filepath = None
        self.username = None
        self.version = "unknown"

    def update(self):
        jeanpaulstart.load_plugins()
        batches = jeanpaulstart.batches_for_user(
            batch_directories=self.batch_directories,
            tags_filepath=self.tags_filepath,
            username=self.username
        )
        self._view.populate_layout(batches)
        self._view.set_version("version " + self.version)

    def show(self):
        self._view.show()

    def batch_clicked(self, batch):
        with HourglassContext(self._view):
            executor = jeanpaulstart.AsyncExecutor(batch)
            executor.message_offset = 1
            executor.start()
            self._view.set_status_message(executor.last_message())

            while executor.status() == jeanpaulstart.ASYNC_EXEC_RUNNING:
                executor.step()
                self._view.set_status_message(_parse_message(executor.last_message()))
                self._view.set_progress(executor.progress())
                self._view.refresh()

            self._view.set_status_message(self.version)
            self._view.set_progress(0)
            self._view.refresh()
