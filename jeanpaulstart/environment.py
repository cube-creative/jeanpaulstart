import os
import constants


def get_env_variable(name):
    return os.environ.get(name)


def set_env_variable(name, value):
    if type(value) == list:
        if constants.OS_IS_WINDOWS:
            value = ';'.join(value)
        else:
            value = ':'.join(value)

    os.environ[name] = os.path.expandvars(str(value))


def parse_env_variable(value):
    if isinstance(value, bool):
        return value

    if constants.OS_IS_WINDOWS:
        return os.path.expandvars(str(value).replace('%', '%%'))

    return os.path.expandvars(str(value))


def parse_env_variables_from_dict(dict_):
    parsed_dict = dict()
    for key, value in dict_.items():
        if isinstance(value, list):
            parsed_dict[key] = [parse_env_variable(item) for item in value]
        elif isinstance(value, dict):
            parsed_dict[key] = {key: parse_env_variable(item) for key, item in value.items()}
        else:
            parsed_dict[key] = parse_env_variable(value)
    return parsed_dict
