import shutil
from StringIO import StringIO
from ConfigParser import ConfigParser, MissingSectionHeaderError
from jeanpaulstart import file_io
from jeanpaulstart.constants import *


TASK_COMMAND = 'ini_file'


class WrongIniContent(RuntimeError):
    pass


class _IniConfigParser(ConfigParser):
    def __init__(self, config_content=None):
        ConfigParser.__init__(self)
        self.optionxform = str

        if config_content is not None:
            self._set_content(config_content)

    def print_content(self):
        result_content = ''
        for section in self.sections():
            result_content = result_content + '[' + section + ']\n'
            if 'None' not in self.options(section):
                for option in self.options(section):
                    result_content = result_content + option + '=' + self.get(section, option) + '\n'
        return result_content

    def _set_content(self, content):
        string_io = StringIO(content)
        try:
            self.readfp(string_io)
        except MissingSectionHeaderError:
            raise WrongIniContent("Given content is not of ini type")

    def _update_content(self, section, state=STATE_PRESENT, option=None, value=None):
        if state == STATE_ABSENT:
            if option is not None:
                self.remove_option(section, option)
            else:
                self.remove_section(section)
        elif state == STATE_PRESENT:
            if not self.has_section(section):
                self.add_section(section)
            self.set(section, option, value)


def _update_ini_content(ini_content, section, state=STATE_PRESENT, option=None, value=None):
    ini_config = _IniConfigParser(ini_content)
    ini_config._update_content(section, state, option, value)
    return ini_config.print_content()


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    return splitted


def apply_(src, section, dest=None, state=STATE_PRESENT, option=None, value=None):
    if dest is not None:
        shutil.copy2(src, dest)
        src = dest

    ini_content = file_io.read_file_utf16(src)

    if option is not None:
        option = option
    if value is not None:
        value = value

    new_ini_content = _update_ini_content(ini_content, section, state, option, value)

    with open(src, 'w+') as ini_file:
        ini_file.write(new_ini_content)

    return OK
