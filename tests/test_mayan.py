# pylint: disable=missing-docstring,pointless-statement

from unittest.mock import patch

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


@patch('mayan_feeder.mayan.MayanHandler.r_get')
def test_is_available(mock_r_get):
    mock_r_get.return_value = {'results': []}

    handler = mayan.MayanHandler(
        'http://foo.bar:81',
        'foo',
        'bar'
    )

    handler.is_available


@patch('mayan_feeder.mayan.MayanHandler.r_get')
def test_is_available_empty_dict(mock_r_get):
    mock_r_get.return_value = {}

    handler = mayan.MayanHandler(
        'http://foo.bar:81',
        'foo',
        'bar'
    )

    with pytest.raises(
        mayan.CouldNotConnect,
        message='Could not connect to http://foo.bar:81'
    ):
        handler.is_available


@patch('mayan_feeder.mayan.MayanHandler.r_get')
def test_is_available_exception(mock_r_get):
    mock_r_get.side_effect = IndexError('foo bar')

    handler = mayan.MayanHandler(
        'http://foo.bar:81',
        'foo',
        'bar'
    )

    with pytest.raises(
        mayan.CouldNotConnect,
        message='Could not connect to http://foo.bar:81'
    ):
        handler.is_available
