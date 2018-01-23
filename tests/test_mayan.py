# pylint: disable=missing-docstring

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


@pytest.mark.parametrize('response,expected', [
    (
        {'info': 'foo'},
        True
    ),
    (
        {},
        False
    )
])
@patch('mayan_feeder.mayan.MayanHandler.r_get')
def test_is_available(mock_r_get, response, expected):
    mock_r_get.return_value = response

    handler = mayan.MayanHandler(
        'http://foo.bar:81',
        'foo',
        'bar'
    )

    assert handler.is_available is expected


@patch('mayan_feeder.mayan.LOG')
@patch('mayan_feeder.mayan.MayanHandler.r_get')
def test_is_available_exception(mock_r_get, mock_log):
    mock_r_get.side_effect = IndexError('foo bar')

    handler = mayan.MayanHandler(
        'http://foo.bar:81',
        'foo',
        'bar'
    )

    assert handler.is_available is False

    mock_log.exception.assert_called_with('foo bar')
