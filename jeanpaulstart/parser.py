import os
import json
from collections import OrderedDict
import yaml


class _OrderedDictYAMLLoader(yaml.Loader):

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)
        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                'expected a mapping node, but found %s' % node.id,
                node.start_mark
            )
        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    'while constructing a mapping',
                    node.start_mark,
                    'found unacceptable key (%s)' % exc,
                    key_node.start_mark
                )
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping


def _norm_slashes(path):
    return path.replace('\\', os.sep).replace('/', os.sep)


def _str_ordered_dict(pairs):
    return OrderedDict(
        [(_str_hook(key, ignore_dicts=True), _str_hook(value, ignore_dicts=True)) for key, value in pairs]
    )


def _str_hook(data, ignore_dicts=False):
    if isinstance(data, unicode):
        return data.encode('utf-8')

    if isinstance(data, list):
        return [_str_hook(item, ignore_dicts=True) for item in data]

    return data


def from_yaml(yaml_content):
    """
    Parses a YAML string
    :param yaml_content:
    :return:
    """
    data = yaml.load(yaml_content, _OrderedDictYAMLLoader)
    return data


def from_json(json_content):
    """
    Parses a JSON string
    :param json_content:
    :return:
    """
    data = _str_hook(
        json.loads(json_content, object_pairs_hook=_str_ordered_dict, object_hook=_str_hook),
        ignore_dicts=True
    )
    return data


def parse(content):
    """
    Tries to parse as YAML, as JSON on failure
    :param content:
    :return:
    """
    try:
        return from_yaml(content)
    except yaml.YAMLError as e:
        return from_json(content)


def _from_json_file(filepath):
    with open(filepath, 'r') as f_json:
        content = f_json.read()

    data = from_json(content)
    return data


def _from_yaml_file(filepath):
    with open(filepath, 'r') as f_yaml:
        content = f_yaml.read()

    data = from_yaml(content)
    return data


def from_file(filepath):
    """
    Parses from a filepath
    Parser is choosen from extension (.json / .yml)
    :param filepath:
    :return: None if file not parsed or doesn't exist or not .json / .yml
    """
    filepath = _norm_slashes(filepath)

    if not os.path.isfile(filepath):
        return None

    if filepath.endswith('.yml'):
        return _from_yaml_file(filepath)

    elif filepath.endswith('.json'):
        return _from_json_file(filepath)


def from_folder(folder):
    """
    Lists all the .json / .yml files in a given folder
    :param folder:
    :return: a list filepathes
    """
    filepathes = list()

    if not os.path.exists(folder):
        return filepathes

    for filename in sorted(os.listdir(folder)):
        filepath = _norm_slashes(os.path.join(folder, filename))

        if not filepath.endswith(('.json', '.yml')): continue
        if not os.path.exists(filepath): continue

        filepathes.append(filepath)

    return filepathes


def from_folders(folders):
    """
    Lists all the .json / .yml files in all the given folders
    :param folders:
    :return: a list filepathes
    """
    filepathes = list()

    for folder in folders:
        filepathes += from_folder(folder)

    return filepathes
