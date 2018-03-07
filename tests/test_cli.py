# pylint: disable=missing-docstring,invalid-name,too-many-arguments

import logging
from unittest.mock import call, patch

import pytest
from click.testing import CliRunner

from mayan_feeder import cli
from mayan_feeder.mayan import CouldNotConnect


@pytest.mark.parametrize('verbose_level,expected', [
    ('-v', logging.INFO),
    ('-vv', logging.DEBUG),
    ('-vvv', logging.DEBUG),
])
@patch('mayan_feeder.cli.threading')
@patch('mayan_feeder.cli.LOG')
@patch('mayan_feeder.cli.utils')
@patch('mayan_feeder.web')
@patch('mayan_feeder.config')
@patch('mayan_feeder.mayan')
def test_main_verbose(
        mock_mayan,
        mock_config,
        mock_web,
        mock_utils,
        mock_log,
        mock_threading,
        verbose_level,
        expected,
        settings,
):
    mock_utils.commands_available.return_value = True
    mock_config.get.return_value = settings
    mock_mayan.MayanHandler.is_available.return_value = None

    runner = CliRunner()

    result = runner.invoke(cli.main, [verbose_level])

    assert result.exit_code == 0

    assert logging.getLogger().getEffectiveLevel() == expected

    mock_threading.Timer.assert_called_with(1.25, mock_utils.open_browser)

    mock_web.SOCKETIO.run.assert_called_with(mock_web.APP)

    assert mock_log.mock_calls == [
        call.debug('Adding timer thread to start Browser...'),
        call.info('Starting the feeder...')
    ]


@patch('mayan_feeder.cli.LOG')
@patch('mayan_feeder.cli.utils')
@patch('mayan_feeder.config')
@patch('mayan_feeder.mayan')
def test_main_couldnotconnect(
        mock_mayan,
        mock_config,
        mock_utils,
        mock_log,
        settings,
):
    mock_utils.commands_available.return_value = True
    mock_config.get.return_value = settings
    mock_mayan.CouldNotConnect = CouldNotConnect
    mock_mayan.MayanHandler.side_effect = CouldNotConnect

    runner = CliRunner()
    result = runner.invoke(cli.main, [])

    assert result.exit_code == 1

    mock_log.error.assert_called_with('Could not connect to MayanEDMS')
