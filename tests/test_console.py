# pylint: disable=missing-docstring, protected-access, redefined-outer-name

from unittest.mock import patch, sentinel

import pytest

from mayan_feeder import console


@pytest.fixture
def console_obj(settings, cabinets_list_0):
    with patch('mayan_feeder.console.mayan') as mock_mayan:
        with patch('mayan_feeder.console.config') as mock_config:

            mock_config.get.return_value = settings
            mock_mayan.MayanHandler().cabinets = cabinets_list_0

            con = console.Console()
            yield con


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


@patch('mayan_feeder.console.radiolist_dialog')
def test_dialog_choose_cabinets(mock_radiolist_dialog, console_obj):
    assert console_obj.dialog_choose_cabinets() == 'main'

    mock_radiolist_dialog.assert_called_with(
        title='Choose cabinet',
        values=[(1, 'Ehmener Str. 30'), (2, 'Gesundheit')]
    )


@pytest.mark.parametrize('cabinets_choosen,text', [
    (None, ''),
    ([2], '<strong>Cabinets</strong>:\nGesundheit')
])
@patch('mayan_feeder.console.button_dialog')
@patch('mayan_feeder.console.HTML')
def test_dialog_main(
        mock_html,
        mock_button_dialog,
        cabinets_choosen,
        text,
        console_obj
):
    con = console_obj
    con._cabinet_dict = {
        1: 'Ehmener Str. 30',
        2: 'Gesundheit'
    }
    con._cabinets_choosen = cabinets_choosen

    mock_html.return_value = 'this is html'

    mock_button_dialog.return_value = sentinel.dialog

    assert con.dialog_main() == sentinel.dialog

    if text:
        mock_html.assert_called_with(text)
        text_arg = 'this is html'
    else:
        text_arg = ''

    mock_button_dialog.assert_called_with(
        title='Mayan-Feeder',
        text=text_arg,
        buttons=[
            ('Add cabinet', 'cabinets'),
            ('Scan', 'scan'),
            ('Reset', 'reset'),
            ('Exit', 'exit')
        ]
    )


@patch('mayan_feeder.console.document.Document')
def test_dialog_scan(mock_document, console_obj):
    con = console_obj
    con._cabinets_choosen = [2]

    assert con.dialog_scan() == 'main'

    mock_document.return_value.process_thread.assert_called()

    mock_document.assert_called_with(
        'http://foo.bar:81',
        'foo',
        'bar',
        [2]
    )


def test_dialog_reset(console_obj):
    con = console_obj
    con._cabinets_choosen = [2]

    assert con.dialog_reset() == 'main'

    assert con._cabinets_choosen == []
