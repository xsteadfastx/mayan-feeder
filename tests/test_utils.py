# pylint: disable=missing-docstring

from unittest.mock import call, patch

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
