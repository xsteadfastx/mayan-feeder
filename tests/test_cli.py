# pylint: disable=missing-docstring,invalid-name,too-many-arguments

import logging
from unittest.mock import call, patch

import pytest
from click.testing import CliRunner

from mayan_feeder import cli


@patch('mayan_feeder.cli.threading')
@patch('mayan_feeder.web')
@patch('mayan_feeder.cli.LOG')
@patch('mayan_feeder.cli.utils')
def test_browser(mock_utils, mock_log, mock_web, mock_threading):

    mock_utils.selfcheck.retuen_value = None

    runner = CliRunner()
    result = runner.invoke(cli.cli, ['browser'])

    assert result.exit_code == 0

    mock_threading.Timer.assert_called_with(1.25, mock_utils.open_browser)

    mock_web.SOCKETIO.run.assert_called_with(mock_web.APP)

    assert mock_log.mock_calls == [
        call.debug('Adding timer thread to start Browser...'),
        call.info('Starting the feeder...')
    ]


# pylint: disable=unused-variable
@pytest.mark.parametrize('verbose_level,expected', [
    ('-v', logging.INFO),
    ('-vv', logging.DEBUG),
    ('-vvv', logging.DEBUG),
])
def test_cli_verbose(verbose_level, expected):

    @cli.cli.command()
    def verbose():
        pass

    runner = CliRunner()
    runner.invoke(cli.cli, [verbose_level, 'verbose'])

    assert logging.getLogger().getEffectiveLevel() == expected
