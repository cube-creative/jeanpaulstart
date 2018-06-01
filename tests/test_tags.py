import copy
from unittest import TestCase
from jeanpaulstart import tags
from jeanpaulstart.batch import parser


YML_TAGS_CONFIG_ON_DISK = """---
developer:
  - p.ho
  - a.tillement
supervisor: 
  - a.tillement
  - t.weyland
graphist:
  - $developer
  - $supervisor
  - a.mondelin
production:
  - $developer
  - c.hergaux
...
"""


BAD_YML_TAGS_CONFIG_ON_DISK = """---
SOME BAD CONTENT
...
"""


EXPECTED_TAGS_CONTENT = {
    'developer': [
        'a.tillement',
        'p.ho'
    ],
    'supervisor': [
        'a.tillement',
        't.weyland'
    ],
    'graphist': [
        '$developer',
        '$supervisor',
        'a.mondelin'
    ],
    'production': [
        '$developer',
        'c.hergaux'
    ]
}

BAD_TAGS_CONTENT = {
    'developer': [
        '$bad-tag',
        'p.ho'
    ]
}


EXPECTED_PARSED_TAGS_CONTENT = {
    'developer': [
        'a.tillement',
        'p.ho'
    ],
    'supervisor': [
        'a.tillement',
        't.weyland'
    ],
    'graphist': [
        'a.mondelin',
        'a.tillement',
        'p.ho',
        't.weyland'
    ],
    'production': [
        'a.tillement',
        'c.hergaux',
        'p.ho'
    ]
}


EXPECTED_USER_TAGS = {
    'a.mondelin': ['graphist'],
    'a.tillement': ['developer', 'graphist', 'production', 'supervisor'],
    'c.hergaux': ['production'],
    'p.ho': ['developer', 'graphist', 'production'],
    't.weyland': ['graphist', 'supervisor']
}


class TestTags(TestCase):

    def test_tags_dict_from_data(self):
        self.maxDiff = None
        data = parser.from_yaml(YML_TAGS_CONFIG_ON_DISK)
        tags_content = tags._tags_dict_from_data(data)

        self.assertDictEqual(
            tags_content,
            EXPECTED_TAGS_CONTENT
        )

    def test_tags_dict_from_bad_data(self):
        data = parser.from_yaml(BAD_YML_TAGS_CONFIG_ON_DISK)
        tags_content = tags._tags_dict_from_data(data)

        self.assertDictEqual(
            tags_content,
            dict()
        )

    def test_parse_group_tags(self):
        tags_content = copy.deepcopy(EXPECTED_TAGS_CONTENT)
        parsed_tags = tags._parse_group_tags(tags_content)

        self.assertDictEqual(
            parsed_tags,
            EXPECTED_PARSED_TAGS_CONTENT
        )

    def test_parse_bad_group_tags(self):
        tags_content = copy.deepcopy(BAD_TAGS_CONTENT)
        parsed_tags = tags._parse_group_tags(tags_content)

        self.assertDictEqual(
            parsed_tags,
            {
                'developer': [
                    'p.ho'
                ]
            }
        )

    def test_load_user_tags(self):
        tags_content=EXPECTED_PARSED_TAGS_CONTENT
        user_tags = tags._load_user_tags_dict(tags_content)

        self.assertDictEqual(
            user_tags,
            EXPECTED_USER_TAGS
        )

    def test_get_one_tag_by_user(self):
        username = 'a.mondelin'

        user_tags = tags.get_tags_by_user(
            user_tags=EXPECTED_USER_TAGS,
            username=username
        )

        self.assertListEqual(
            user_tags,
            ['common', 'graphist']
        )

    def test_get_multiple_tags_by_user(self):
        username = 'p.ho'

        user_tags = tags.get_tags_by_user(
            user_tags=EXPECTED_USER_TAGS,
            username=username
        )

        self.assertListEqual(
            user_tags,
            ['common', 'developer', 'graphist', 'production']
        )

    def test_get_tags_by_bad_user(self):
        username = 'some-bad-name'

        user_tags = tags.get_tags_by_user(
            user_tags=EXPECTED_USER_TAGS,
            username=username
        )

        self.assertListEqual(
            user_tags,
            ['common']
        )

    def test_get_tags_by_bad_user_without_common(self):
        username = 'some-bad-name'

        user_tags = tags.get_tags_by_user(
            user_tags=EXPECTED_USER_TAGS,
            username=username,
            include_common=False
        )

        self.assertListEqual(
            user_tags,
            []
        )
