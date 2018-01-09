# pylint: disable=missing-docstring

from unittest.mock import call, patch

import pytest

from mayan_feeder import utils


@patch('mayan_feeder.utils.LOG')
@patch('mayan_feeder.utils.os')
def test_chdir(mock_os, mock_log):
    mock_os.getcwd.return_value = '/tmp/bar'

    with utils.ChDir('/tmp/foo'):
        pass

    assert mock_os.chdir.call_args_list == [
        call('/tmp/foo'),
        call('/tmp/bar')
    ]

    assert mock_log.debug.call_args_list == [
        call('enter %s...', '/tmp/foo'),
        call('enter %s again...', '/tmp/bar')
    ]


@pytest.mark.parametrize('commands,expected', [
    (
        [True, True],
        True
    ),
    (
        [False, True],
        False
    )
])
@patch('mayan_feeder.utils.spawn')
def test_commands_available(mock_spawn, commands, expected):
    mock_spawn.find_executable.side_effect = commands

    assert utils.commands_available(['foo', 'bar']) == expected
