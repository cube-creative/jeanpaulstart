from batch import parser


def load_by_user(tags_filepath, username):
    tags_data = parser._from_yaml_file(tags_filepath)
    tags_dict = _tags_dict_from_data(tags_data)
    parsed_tags = _parse_group_tags(tags_dict)

    return get_tags_by_user(
        user_tags=_load_user_tags_dict(parsed_tags),
        username=username
    )


def get_tags_by_user(user_tags, username, include_common=True):
    tags_list = list()

    if include_common:
        tags_list.append('common')

    if not user_tags or username not in user_tags.keys():
        return tags_list

    tags_list.extend(user_tags[username])
    return tags_list


def _tags_dict_from_data(tags_data):
    if not isinstance(tags_data, dict):
        return dict()

    tags_dict = dict()

    for tag, user_list in tags_data.items():
        tags_dict[tag] = sorted(user_list)

    return tags_dict


def _parse_group_tags(tags_dict):
    parsed_dict = dict(tags_dict)

    for tag in parsed_dict.keys():
        matching_tags = [s for s in parsed_dict[tag] if "$" in s]
        for matching_tag in matching_tags:
            parsed_dict[tag].remove(matching_tag)
            if matching_tag[1:] in parsed_dict.keys():
                parsed_users = [x for x in parsed_dict[matching_tag[1:]] if x not in parsed_dict[tag]]
                parsed_dict[tag].extend(parsed_users)

                parsed_dict[tag] = sorted(parsed_dict[tag])

    return parsed_dict


def _load_user_tags_dict(tags_content):
    user_tags_dict = dict()
    for tag, user_list in tags_content.items():
        for user in user_list:
            if user not in user_tags_dict.keys():
                user_tags_dict[user] = list()

            user_tags_dict[user].append(tag)
            user_tags_dict[user].sort()

    return user_tags_dict
