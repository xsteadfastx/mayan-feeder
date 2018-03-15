# pylint: disable=missing-docstring, protected-access

from unittest.mock import patch

import pytest

from mayan_feeder import console


@pytest.fixture
def console_obj():
    pass


@patch('mayan_feeder.console.mayan')
@patch('mayan_feeder.console.config')
def test_init(mock_config, mock_mayan, settings, cabinets_list_0):
    mock_config.get.return_value = settings
    mock_mayan.MayanHandler().cabinets = cabinets_list_0

    con = console.Console()

    assert con._cabinet_dict == {1: 'Ehmener Str. 30', 2: 'Gesundheit'}

    assert con._cabinets_available == [
        (1, 'Ehmener Str. 30'),
        (2, 'Gesundheit')
    ]

    mock_mayan.MayanHandler.assert_called_with(
        'http://foo.bar:81',
        'foo',
        'bar'
    )


def test_dialog_choose_cabinets():
    pass
