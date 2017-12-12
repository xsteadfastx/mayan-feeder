# pylint: disable=missing-docstring

import pytest


@pytest.fixture
def cabinets_list_0():
    yield {
        'count': 2,
        'next': None,
        'previous': None,
        'results': [
            {
                'children': [],
                'documents_count': 13,
                'documents_url': (
                    'http://192.168.39.115:81'
                    '/api/cabinets/cabinets/1/documents/'
                ),
                'full_path': 'Ehmener Str. 30',
                'id': 1,
                'label': 'Ehmener Str. 30',
                'parent': None,
                'parent_url': '',
                'url': 'http://192.168.39.115:81/api/cabinets/cabinets/1/'},
            {
                'children': [],
                'documents_count': 4,
                'documents_url': (
                    'http://192.168.39.115:81'
                    '/api/cabinets/cabinets/2/documents/'
                ),
                'full_path': 'Gesundheit',
                'id': 2,
                'label': 'Gesundheit',
                'parent': None,
                'parent_url': '',
                'url': 'http://192.168.39.115:81/api/cabinets/cabinets/2/'
            }
        ]
    }


@pytest.fixture
def document_config():
    yield [
        'http://foo.bar:81',
        'admin',
        'barfoo',
        ['1']
    ]


@pytest.fixture
def settings():
    yield {
        'mayan': {
            'url': 'http://foo.bar:81',
            'username': 'foo',
            'password': 'bar'
        }
    }
