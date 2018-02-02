# pylint: disable=missing-docstring

from unittest.mock import patch


@patch('mayan_feeder.forms.create_cabinets')
def test_root_get(mock_create_cabinets, web_app):
    mock_create_cabinets.return_value = [
        ('1', 'Foo'),
        ('2', 'Bar'),
    ]

    response = web_app.get('/')

    assert response.status_code == 200

    assert (
        b'<option value="1">Foo</option>'
        b'<option value="2">Bar</option>'
    ) in response.data


@patch('mayan_feeder.forms.create_cabinets')
@patch('mayan_feeder.config.get')
@patch('mayan_feeder.document.Document')
def test_root_post(
        mock_document,
        mock_config,
        mock_create_cabinets,
        web_app,
        settings
):
    mock_create_cabinets.return_value = [
        ('1', 'Foo'),
        ('2', 'Bar'),
    ]

    mock_config.return_value = settings

    response = web_app.post('/', data={'cabinets': '1'})

    assert response.status_code == 200

    mock_document.assert_called_with(
        'http://foo.bar:81',
        'foo',
        'bar',
        ['1']
    )

    mock_document.return_value.process.assert_called()
