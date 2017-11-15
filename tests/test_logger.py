# pylint: disable=missing-docstring

import logging
from unittest.mock import patch

import pytest

from mayan_feeder import logger


@pytest.mark.parametrize('level,expected', [
    (
        'INFO',
        'success'
    ),
    (
        'DEBUG',
        'info'
    ),
    (
        'WARNING',
        'warning'
    ),
    (
        'CRITICAL',
        'danger'
    ),
    (
        'ERROR',
        'danger'
    ),
    (
        'EXCEPTION',
        'danger'
    ),
    (
        'FOOBAR',
        'muted'
    ),
])
def test__colorize_it(level, expected):
    record = logging.makeLogRecord(
        {
            'levelname': level,
            'msg': 'foo'
        }
    )

    # pylint: disable=protected-access
    assert logger.SocketIOHandler()._colorize_it(
        record
    ) == {
        'class': expected,
        'msg': 'foo'
    }


@patch('mayan_feeder.logger.web')
def test_emit(mock_web):
    logger.SocketIOHandler().emit(
        logging.makeLogRecord(
            {
                'levelname': 'INFO',
                'msg': 'foo',
                'name': 'mayan_feeder'
            })
    )

    mock_web.SOCKETIO.emit.assert_called_with(
        'my response',
        {
            'class': 'success',
            'msg': 'foo'
        },
        json=True,
        namespace='/feeder'
    )


@patch('mayan_feeder.logger.web')
def test_emit_not_called(mock_web):
    logger.SocketIOHandler().emit(
        logging.makeLogRecord(
            {
                'levelname': 'INFO',
                'msg': 'foo',
                'name': 'socketio'
            })
    )

    mock_web.SOCKETIO.emit.assert_not_called()
