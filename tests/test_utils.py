# pylint: disable=missing-docstring, invalid-name

import os
import re
from ast import literal_eval
from unittest.mock import call, patch

import pytest

from mayan_feeder import utils
from mayan_feeder.mayan import CouldNotConnect


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


@pytest.mark.parametrize('image_file', [
    'out1_False.jpg',
    'out2_True.jpg',
])
def test_is_blank(image_file):
    re_expected = r'out\d_(True|False).jpg'
    expected = literal_eval(re.search(re_expected, image_file).group(1))

    file_full_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        image_file
    )

    assert utils.is_blank(file_full_path) == expected


@patch('mayan_feeder.utils.LOG')
@patch('mayan_feeder.utils.commands_available')
def test_selfcheck_commands_not_available(mock_commands_available, mock_log):
    mock_commands_available.return_value = False

    with pytest.raises(SystemExit) as excinfo:
        utils.selfcheck()

    assert excinfo.value.code == 1

    assert mock_commands_available.call_args_list == [
        call(['scanimage', 'tiffcp', 'tiff2pdf'])
    ]

    assert mock_log.error.call_args_list == [
        call(
            (
                'Could not find needed commands! '
                'Please install convert and scanimage'
            )
        )
    ]


@patch('mayan_feeder.utils.mayan')
@patch('mayan_feeder.utils.config')
@patch('mayan_feeder.utils.commands_available')
@patch('mayan_feeder.utils.LOG')
def test_selfcheck_coulnotconnect(
        mock_log,
        mock_commands_available,
        mock_config,
        mock_mayan,
        settings
):
    mock_commands_available.return_value = True
    mock_config.get.return_value = settings
    mock_mayan.CouldNotConnect = CouldNotConnect
    mock_mayan.MayanHandler.side_effect = CouldNotConnect

    with pytest.raises(SystemExit) as excinfo:
        utils.selfcheck()

    assert excinfo.value.code == 1

    mock_log.error.assert_called_with('Could not connect to MayanEDMS')
