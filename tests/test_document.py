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
