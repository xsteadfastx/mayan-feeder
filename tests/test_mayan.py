# pylint: disable=missing-docstring

import pytest

from mayan_feeder import mayan


@pytest.mark.parametrize('endpoint,expected', [
    (
        '/api/foo',
        'http://foo.bar:81/api/foo'
    ),
])
def test_create_url(endpoint, expected):
    handler = mayan.MayanHandler(
        'http://foo.bar:81',
        'foo',
        'bar'
    )

    assert handler.create_url(endpoint) == expected
