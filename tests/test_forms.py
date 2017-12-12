# pylint: disable=missing-docstring

from unittest.mock import patch

from data import CABINETS_LIST_0

from mayan_feeder import forms, web
from utils import SETTINGS


@patch('mayan_feeder.forms.mayan', autospec=True)
@patch('mayan_feeder.forms.config', autospec=True)
def test_create_cabinets(mock_config, mock_mayan):
    mock_config.get.return_value = SETTINGS
    mock_mayan.MayanHandler.return_value.cabinets.return_value = \
        CABINETS_LIST_0

    assert forms.create_cabinets() == [
        ('1', 'Ehmener Str. 30'),
        ('2', 'Gesundheit')
    ]


@patch('mayan_feeder.forms.config', autospec=True)
def test_create_cabinets_no_config(mock_config):
    mock_config.get.return_value = None

    assert forms.create_cabinets() is None


@patch('mayan_feeder.forms.create_cabinets', autospec=True)
def test_document_form(mock_create_cabinets):
    mock_create_cabinets.return_value = [
        ('1', 'Foo Bar')
    ]

    web.APP.config['SECRET_KEY'] = 'foobar'

    with web.APP.app_context():
        with web.APP.test_request_context():

            form = forms.DocumentForm()

            assert form.cabinets.choices == [('1', 'Foo Bar')]
