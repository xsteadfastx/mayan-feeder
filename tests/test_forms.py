# pylint: disable=missing-docstring

from unittest.mock import patch

from data import CABINETS_LIST_0

from mayan_feeder import forms
from utils import SETTINGS


@patch('mayan_feeder.forms.mayan')
@patch('mayan_feeder.forms.config')
def test_create_cabinets(mock_config, mock_mayan):
    mock_config.get.return_value = SETTINGS
    mock_mayan.MayanHandler.return_value.cabinets.return_value = \
        CABINETS_LIST_0

    assert forms.create_cabinets() == [
        ('1', 'Ehmener Str. 30'),
        ('2', 'Gesundheit')
    ]
