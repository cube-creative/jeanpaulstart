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
            except TypeError, exc:
                raise yaml.constructor.ConstructorError(
                    'while constructing a mapping',
                    node.start_mark,
                    'found unacceptable key (%s)' % exc,
                    key_node.start_mark
                )
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping


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
    data = yaml.load(yaml_content, _OrderedDictYAMLLoader)
    return data


def from_json(json_content):
    data = _str_hook(
        json.loads(json_content, object_pairs_hook=_str_ordered_dict, object_hook=_str_hook),
        ignore_dicts=True
    )
    return data


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
    if not os.path.isfile(filepath):
        return None

    if filepath.endswith('.yml'):
        return _from_yaml_file(filepath)

    elif filepath.endswith('.json'):
        return _from_json_file(filepath)


def from_folder(folder):
    data = list()

    if not os.path.exists(folder):
        return data

    for filename in sorted(os.listdir(folder)):
        filepath = os.path.join(folder, filename).replace('\\', '/')
        file_data = from_file(filepath)
        if file_data:
            data.append((filepath, file_data))

    return data


def from_folders(folders):
    data = list()

    for folder in folders:
        data += from_folder(folder)

    return data
