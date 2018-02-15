# pylint: disable=missing-docstring

from unittest.mock import patch

from mayan_feeder import forms, web


@patch('mayan_feeder.forms.mayan', autospec=True)
@patch('mayan_feeder.forms.config', autospec=True)
def test_create_cabinets(mock_config, mock_mayan, cabinets_list_0, settings):
    mock_config.get.return_value = settings
    mock_mayan.MayanHandler.return_value.cabinets = \
        cabinets_list_0

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
