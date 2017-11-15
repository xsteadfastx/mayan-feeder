# pylint: disable=missing-docstring

from pathlib import Path
from unittest.mock import call, patch

import pytest
import yaml

from mayan_feeder import config


@pytest.mark.parametrize('config_data,expected', [
    (
        {
            'mayan': {
                'url': 'http://foo.bar:81',
                'username': 'foobar',
                'password': 'barfoo',
            }
        },
        {
            'mayan': {
                'url': 'http://foo.bar:81',
                'username': 'foobar',
                'password': 'barfoo',
            }
        },
    ),
])
@patch('mayan_feeder.config.LOG')
@patch('mayan_feeder.config.Path')
def test_get(mock_path, mock_log, config_data, expected, tmpdir):
    mock_path.home.return_value = Path(tmpdir.strpath)

    config_file = tmpdir.join('.mayanfeeder.yaml')
    config_file.write(yaml.dump(config_data))

    assert config.get() == expected

    assert mock_log.debug.call_args_list == [
        call('Parsing config file...'),
        call('Parsed config: %s', expected)
    ]


@patch('mayan_feeder.config.Path')
@patch('mayan_feeder.config.echo')
def test_get_no_configfile(mock_echo, mock_path):
    mock_path.home.return_value.joinpath.return_value.exists.return_value = \
        False

    with pytest.raises(SystemExit):
        config.get()

    mock_echo.assert_called_with('No configfile found!')


@pytest.mark.parametrize('config_data', [
    (
        {
            'mayan': {
                'username': 'foobar',
                'password': 'barfoo',
            }
        }
    ),
    (
        {
            'mayan': {
                'url': 'http://foo.bar:81',
                'password': 'barfoo',
            }
        }
    ),
    (
        {
            'mayan': {
                'url': 'http://foo.bar:81',
                'username': 'foobar',
            }
        }
    ),
])
@patch('mayan_feeder.config.echo')
@patch('mayan_feeder.config.Path')
def test_get_missing_mayan_keys(
        mock_path,
        mock_echo,
        config_data,
        tmpdir
):
    mock_path.home.return_value = Path(tmpdir.strpath)

    config_file = tmpdir.join('.mayanfeeder.yaml')
    config_file.write(yaml.dump(config_data))

    with pytest.raises(SystemExit):
        config.get()

    mock_echo.assert_called_with(
        'Missing url, username or password in mayan settings!'
    )
