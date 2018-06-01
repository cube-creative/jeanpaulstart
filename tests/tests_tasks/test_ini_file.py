import unittest
from copy import deepcopy
from jeanpaulstart.tasks import ini_file
from jeanpaulstart.constants import *


VARIABLE_NAME = 'VARIABLE_NAME'
VARIABLE_VALUE = 'MICHEL'
INI_CONFIG_CONTENT = """[SectionOne]
Name=Michel
[SectionTwo]
ConfigName=SomeValue
OtherName=OtherValue
"""
USER_DATA = {
    'name': 'Task Name',
    'ini_file': {
        'src': 'src',
        'section': 'section',
        'dest': 'dest',
        'state': 'state',
        'option': 'option',
        'value': 'value'
    }
}
SPLITTED = {
    'name': 'Task Name',
    'command': 'file',
    'arguments': {
        'src': 'src',
        'section': 'section',
        'dest': 'dest',
        'state': 'state',
        'option': 'option',
        'value': 'value'
    }
}


class TestTaskIniFile(unittest.TestCase):

    def test_ini_bad_content(self):
        with self.assertRaises(ini_file.WrongIniContent):
            ini_file._update_ini_content(
                ini_content='Some-broken-content',
                state='present',
                section='NewSection'
            )

    def test_ini_set_new_section(self):
        new_ini_content = ini_file._update_ini_content(
            ini_content=INI_CONFIG_CONTENT,
            state='present',
            section='NewSection',
            option=VARIABLE_NAME,
            value=VARIABLE_VALUE
        )

        self.assertEqual(
            new_ini_content,
            """[SectionOne]
Name=Michel
[SectionTwo]
ConfigName=SomeValue
OtherName=OtherValue
[NewSection]
VARIABLE_NAME=MICHEL
"""
        )

    def test_ini_del_section(self):
        new_ini_content = ini_file._update_ini_content(
            ini_content=INI_CONFIG_CONTENT,
            state='absent',
            section='SectionTwo'
        )
        self.assertEqual(
            new_ini_content,
            """[SectionOne]
Name=Michel
"""
        )

    def test_ini_set_option_in_existing_section(self):
        new_ini_content = ini_file._update_ini_content(
            ini_content=INI_CONFIG_CONTENT,
            state='present',
            section='SectionTwo',
            option=VARIABLE_NAME,
            value=VARIABLE_VALUE
        )

        self.assertEqual(
            new_ini_content,
            """[SectionOne]
Name=Michel
[SectionTwo]
ConfigName=SomeValue
OtherName=OtherValue
VARIABLE_NAME=MICHEL
"""
        )

    def test_ini_replace_option(self):
        new_ini_content = ini_file._update_ini_content(
            ini_content=INI_CONFIG_CONTENT,
            state='present',
            section='SectionTwo',
            option='ConfigName',
            value=VARIABLE_VALUE
        )

        self.assertEqual(
            new_ini_content,
            """[SectionOne]
Name=Michel
[SectionTwo]
ConfigName=MICHEL
OtherName=OtherValue
"""
        )

    def test_ini_delete_option(self):
        new_ini_content = ini_file._update_ini_content(
            ini_content=INI_CONFIG_CONTENT,
            state='absent',
            section='SectionTwo',
            option='ConfigName'
        )

        self.assertEqual(
            new_ini_content,
            """[SectionOne]
Name=Michel
[SectionTwo]
OtherName=OtherValue
"""
        )

    def test_validate(self):
        status, message = ini_file.validate(USER_DATA)
        self.assertEqual(
            status,
            OK
        )

    def test_normalize(self):
        normalized = ini_file.normalize_after_split(deepcopy(SPLITTED))

        self.assertDictEqual(
            normalized,
            SPLITTED
        )

    #TODO : Ecrire les tests pour apply()
