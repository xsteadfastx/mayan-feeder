# pylint: disable=missing-docstring

from datetime import datetime
from unittest.mock import patch

from data import DOCUMENT_CONFIG

from mayan_feeder.document import Document


@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
@patch('mayan_feeder.document.mayan.MayanHandler', autospec=True)
@patch('mayan_feeder.document.datetime', autospec=True)
def test_init(mock_datetime, mock_mayan_handler, mock_mkdtemp):
    mock_datetime.now.return_value = datetime(2017, 12, 8, 0, 0, 0, 0)
    mock_mkdtemp.return_value = '/tmp/footmp'

    document = Document(*DOCUMENT_CONFIG)

    mock_mayan_handler.assert_called_with(
        'http://foo.bar:81',
        'admin',
        'barfoo'
    )

    assert document.url == 'http://foo.bar:81'
    assert document.username == 'admin'
    assert document.password == 'barfoo'
    assert document.cabinets == ['1']
    assert document.now == datetime(2017, 12, 8, 0, 0)
    assert document.pdf_filename == '20170008000000.pdf'
    assert document.tempdir == '/tmp/footmp'
    assert document.pdf_file_path == '/tmp/footmp/20170008000000.pdf'


@patch('mayan_feeder.document.mayan.MayanHandler', autospec=True)
def test_upload(mock_mayan_handler):
    mock_mayan_handler.return_value.upload.return_value = {
        'id': 77
    }

    document = Document(*DOCUMENT_CONFIG)
    document.upload()

    assert document.document_id == 77


@patch('mayan_feeder.document.mayan.MayanHandler', autospec=True)
@patch('mayan_feeder.document.LOG', autospec=True)
def test_upload_exception(mock_log, mock_mayan_handler):
    mock_mayan_handler.return_value.upload.side_effect = IndexError('foo')

    document = Document(*DOCUMENT_CONFIG)
    document.upload()

    mock_log.exception.assert_called_with('foo')


@patch('mayan_feeder.document.mayan.MayanHandler', autospec=True)
@patch('mayan_feeder.document.LOG', autospec=True)
def test_add_to_cabinets(mock_log, mock_mayan_handler):
    mock_mayan_handler.return_value.upload.return_value = {
        'id': 77
    }

    document = Document(*DOCUMENT_CONFIG)
    document.upload()

    document.add_to_cabinets()

    mock_log.debug.assert_called_with(
        'adding to cabinet %s...',
        '1'
    )

    mock_mayan_handler.return_value.add_to_cabinet.assert_called_with(
        '1',
        77
    )


@patch('mayan_feeder.document.mayan.MayanHandler', autospec=True)
@patch('mayan_feeder.document.LOG', autospec=True)
def test_add_to_cabinets_exception(mock_log, mock_mayan_handler):
    mock_mayan_handler.return_value.add_to_cabinet.side_effect = \
        IndexError('foo')

    document = Document(*DOCUMENT_CONFIG)
    document.upload()
    document.add_to_cabinets()

    mock_log.exception.assert_called_with('foo')
