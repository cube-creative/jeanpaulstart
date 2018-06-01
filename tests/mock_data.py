from jeanpaulstart import constants
from collections import OrderedDict


TAGS_FILE_CONTENT = """---
tag1:
  - t.est
...
"""


TASK_ENV = {
    'name': 'From environment',
    'command': 'environment',
    'arguments': {
        'name': 'ENV_VAR_1',
        'value': 'value1'
    },
    'ignore_errors': False,
    'register_status': False
}


TASK_ENV_LIST = {
    'name': 'From environment',
    'command': 'environment',
    'arguments': {
        'name': 'ENV_VAR_2',
        'value': ['valuea', 'valueb']
    },
    'ignore_errors': False,
    'register_status': False
}


TASK_INI = {
    'name': 'Some Name',
    'command': 'ini_file',
    'arguments': {
        'dest': r'path/to/inifile',
        'state': constants.STATE_PRESENT,
        'section': 'SectionTwo',
        'option': 'option1',
        'value': 'value1'
    },
    'ignore_errors': False
}


TASK_RAW = {
    'name': 'Some Name',
    'command': 'raw',
    'arguments': {
        'command': r'some\random\path',
        'async': True
    },
    'ignore_errors': True
}


TASK_TEMPLATE = {
    'name': 'Some Name',
    'command': 'template',
    'arguments': {
        'src': r'some\template\path',
        'dest': r'some\destination\path',
        'force': True
    },
    'ignore_errors': False
}


TASK_URL = {
    'name': 'Some Name',
    'command': 'url',
    'arguments': {
        'url': r'some\url'
    },
    'ignore_errors': False
}


TASK_COPY = {
    'name': 'Some Name',
    'command': 'copy',
    'arguments': {
        'src': r'path\source',
        'dest': r'path\dest',
        'force': True
    },
    'ignore_errors': False
}


TASK_FILE = {
    'name': 'Some Name',
    'command': 'file',
    'arguments': {
        'path': 'some/path',
        'state': 'directory'
    },
    'ignore_errors': False
}


TASK_PIP = {
    'name': 'Some Name',
    'command': 'pip',
    'arguments': {
        'name': 'some/lib',
        'state': constants.STATE_PRESENT
    },
    'ignore_errors': False
}


BATCH_YAML_CONTENT = r"""---
name: Yaml Name
icon_path: some/icon/path
tags:
  - tag1
  - tag2
environment:
  ENV_VAR1: value1
  ENV_VAR2: 
    - valuea
    - valueb

tasks:
  - name: Some Task
    raw: 
      command: some command
      async: false
..."""


BATCH_JSON_CONTENT = r"""{
    "name": "JSON Name",
    "icon_path": "some/icon/path",
    "tags": ["tag3", "tag4"],
    "environment": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": ["valuea", "valueb"]
    },
    "tasks": [
        {"name": "Some Task", "raw": {"command": "some command", "async": false}}
    ]
}"""


BATCH_JSON_CONTENT_NORMALIZED = r"""{
    "name": "JSON Name",
    "icon_path": "some/icon/path",
    "tags": ["tag3", "tag4", "admin"],
    "tasks": [
        {
            "name": "From environment", 
            "command": "environment", 
            "arguments": {
                "name": "ENV_VAR1", 
                "value": "value1"
            },
            "ignore_errors": false,
            "register_status": false
        }, 
        {
            "name": "From environment", 
            "command": "environment", 
            "arguments": {
                "name": "ENV_VAR2", 
                "value": [
                    "valuea", 
                    "valueb"
                ]
            },
            "ignore_errors": false,
            "register_status": false
        }, 
        {
            "name": "Some Task", 
            "command": "raw", 
            "arguments": {
                "command": "some command",
                "async": false
            },
            "ignore_errors": false,
            "register_status": false
        }
    ]
}"""


BATCH_JSON_CONTENT_NOT_VALID = r"""{
    "icon_path": "some/icon/path",
    "tags": ["tag3", "tag4"],
    "environment": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": ["valuea", "valueb"]
    },
    "tasks": [
        {"name": "Some Task", "raw": {"command": "some command", "async": "False"}}
    ]
}"""


DUMPED_NORMALIZED = '"{\\"name\\": \\"JSON Name\\", \\"icon_path\\": \\"some/icon/path\\", \\"tags\\": [\\"tag3\\", \\"tag4\\", \\"admin\\"], \\"tasks\\": [{\\"ignore_errors\\": false, \\"register_status\\": false, \\"command\\": \\"environment\\", \\"name\\": \\"From environment\\", \\"arguments\\": {\\"name\\": \\"ENV_VAR1\\", \\"value\\": \\"value1\\"}}, {\\"ignore_errors\\": false, \\"register_status\\": false, \\"command\\": \\"environment\\", \\"name\\": \\"From environment\\", \\"arguments\\": {\\"name\\": \\"ENV_VAR2\\", \\"value\\": [\\"valuea\\", \\"valueb\\"]}}, {\\"ignore_errors\\": false, \\"register_status\\": false, \\"command\\": \\"raw\\", \\"name\\": \\"Some Task\\", \\"arguments\\": {\\"command\\": \\"some command\\", \\"async\\": false}}]}"'
DUMPED_NOT_NORMALIZED = '"{\\"name\\": \\"JSON Name\\", \\"icon_path\\": \\"some/icon/path\\", \\"tags\\": [\\"tag3\\", \\"tag4\\"], \\"environment\\": {\\"ENV_VAR1\\": \\"value1\\", \\"ENV_VAR2\\": [\\"valuea\\", \\"valueb\\"]}, \\"tasks\\": [{\\"name\\": \\"Some Task\\", \\"raw\\": {\\"command\\": \\"some command\\", \\"async\\": false}}]}"'


def _batch_not_normalized(name, tags_3_4=False):
    batch = OrderedDict()
    batch['name'] = name
    batch['icon_path'] = 'some/icon/path'
    batch['tags'] = ['tag3', 'tag4'] if tags_3_4 else ['tag1', 'tag2']
    batch['environment'] = OrderedDict()
    batch['environment']['ENV_VAR1'] = 'value1'
    batch['environment']['ENV_VAR2'] = ['valuea', 'valueb']
    batch['tasks'] = [OrderedDict()]
    batch['tasks'][0]['name'] = 'Some Task'
    batch['tasks'][0]['raw'] = {'command': 'some command', 'async': False}
    return batch


#OrderedDict([('name', 'JSON Name'), ('icon_path', 'some/icon/path'), ('tags', ['tag3', 'tag4', 'admin']), ('tasks', [OrderedDict([('name', 'From environment'), ('command', 'environment'), ('arguments', OrderedDict([('name', 'ENV_VAR1'), ('value', 'value1')])), ('ignore_errors', False)]), OrderedDict([('name', 'From environment'), ('command', 'environment'), ('arguments', OrderedDict([('name', 'ENV_VAR2'), ('value', ['valuea', 'valueb'])])), ('ignore_errors', False)]), OrderedDict([('name', 'Some Task'), ('command', 'raw'), ('arguments', OrderedDict([('command', 'some command'), ('async', False)])), ('ignore_errors', False)])])]) != OrderedDict([('name', 'JSON Name'), ('icon_path', 'some/icon/path'), ('tags', ['tag3', 'tag4', 'admin']), ('tasks', [{'ignore_errors': False, 'register_status': False, 'command': 'environment', 'name': 'From environment', 'arguments': {'name': 'ENV_VAR1', 'value': 'value1'}}, {'ignore_errors': False, 'register_status': False, 'command': 'environment', 'name': 'From environment', 'arguments': {'name': 'ENV_VAR2', 'value': ['valuea', 'valueb']}}, {'ignore_errors': False, 'register_status': False, 'command': 'raw', 'name': 'Some Task', 'arguments': {'async': False, 'command': 'some command'}}])])
def _batch(name, tags_3_4=False, register_status_for_raw=False):
    batch = OrderedDict()
    batch['name'] = name
    batch['icon_path'] = 'some/icon/path'
    batch['tags'] = ['tag3', 'tag4', constants.TAG_ADMIN] if tags_3_4 else ['tag1', 'tag2', constants.TAG_ADMIN]
    batch['tasks'] = [
        {
            'name': 'From environment',
            'command': 'environment',
            'ignore_errors': False,
            'register_status': False,
            'arguments': {'name': 'ENV_VAR1', 'value': 'value1'}
        },
        {
            'name': 'From environment',
            'command': 'environment',
            'ignore_errors': False,
            'register_status': False,
            'arguments': {'name': 'ENV_VAR2', 'value': ['valuea', 'valueb']}
        },
        {
            'name': 'Some Task',
            'command': 'raw',
            'ignore_errors': False,
            'register_status': register_status_for_raw,
            'arguments': {'command': 'some command', 'async': False}
        }
    ]
    return batch


def _expected_batches():
    yaml_batch = _batch('Yaml Name')
    json_batch = _batch('JSON Name', tags_3_4=True)
    return [yaml_batch, json_batch]


NORMALIZED_ENV_TASKS = [TASK_ENV, TASK_ENV_LIST]
