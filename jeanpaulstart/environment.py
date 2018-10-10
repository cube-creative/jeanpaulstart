import os
import re
import platform


_REGEX = re.compile(r"\$[^\"\\' +!=.]+")


def get(name):
    return os.environ.get(name)


def set(name, value):
    if type(value) == list:
        if platform.system() == 'Windows':
            value = ';'.join(value)
        else:
            value = ':'.join(value)

    os.environ[name] = os.path.expandvars(str(value))


def parse_expression(expression):
    parsed = expression

    for match in _REGEX.findall(expression):
        value = os.environ.get(match[1:], match)
        parsed = parsed.replace(match, "'{}'".format(value))

    return parsed


def parse(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, dict):
        return _parse_from_dict(value)

    if platform.system() == 'Windows':
        return os.path.expandvars(str(value).replace('%', '%%'))

    return os.path.expandvars(str(value))


def _parse_from_dict(dict_):
    parsed_dict = dict()
    for key, value in dict_.items():
        key = parse(key)

        if isinstance(value, list):
            parsed_dict[key] = [parse(item) for item in value]

        elif isinstance(value, dict):
            parsed_dict[key] = {key: parse(item) for key, item in value.items()}

        else:
            parsed_dict[key] = parse(value)

    return parsed_dict
