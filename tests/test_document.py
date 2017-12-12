# pylint: disable=missing-docstring

from datetime import datetime
from unittest.mock import call, patch

from mayan_feeder.document import Document


@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
@patch('mayan_feeder.document.mayan.MayanHandler', autospec=True)
@patch('mayan_feeder.document.datetime', autospec=True)
def test_init(
        mock_datetime,
        mock_mayan_handler,
        mock_mkdtemp,
        document_config
):
    mock_datetime.now.return_value = datetime(2017, 12, 8, 0, 0, 0, 0)
    mock_mkdtemp.return_value = '/tmp/footmp'

    document = Document(*document_config)

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
def test_upload(mock_mayan_handler, document_config):
    mock_mayan_handler.return_value.upload.return_value = {
        'id': 77
    }

    document = Document(*document_config)
    document.upload()

    assert document.document_id == 77


@patch('mayan_feeder.document.mayan.MayanHandler', autospec=True)
@patch('mayan_feeder.document.LOG', autospec=True)
def test_upload_exception(mock_log, mock_mayan_handler, document_config):
    mock_mayan_handler.return_value.upload.side_effect = IndexError('foo')

    document = Document(*document_config)
    document.upload()

    mock_log.exception.assert_called_with('foo')


@patch('mayan_feeder.document.mayan.MayanHandler', autospec=True)
@patch('mayan_feeder.document.LOG', autospec=True)
def test_add_to_cabinets(mock_log, mock_mayan_handler, document_config):
    mock_mayan_handler.return_value.upload.return_value = {
        'id': 77
    }

    document = Document(*document_config)
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
def test_add_to_cabinets_exception(
        mock_log,
        mock_mayan_handler,
        document_config
):
    mock_mayan_handler.return_value.add_to_cabinet.side_effect = \
        IndexError('foo')

    document = Document(*document_config)
    document.upload()
    document.add_to_cabinets()

    mock_log.exception.assert_called_with('foo')


@patch('mayan_feeder.document.Thread', autospec=True)
@patch('mayan_feeder.document.LOG', autospec=True)
def test_process(mock_log, mock_thread, document_config):
    document = Document(*document_config)
    document.process()

    mock_log.debug.assert_called_with('starting thread...')
    mock_thread.return_value.start.assert_called()


# pylint: disable=too-many-arguments
@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
@patch('mayan_feeder.document.Document.add_to_cabinets')
@patch('mayan_feeder.document.Document.upload')
@patch('mayan_feeder.document.Document.create_pdf')
@patch('mayan_feeder.document.Document.scanning')
@patch('mayan_feeder.document.LOG')
@patch('mayan_feeder.document.rmtree')
@patch('mayan_feeder.document.sleep')
def test_process_thread(
        mock_sleep,
        mock_rmtree,
        mock_log,
        mock_scanning,
        mock_create_pdf,
        mock_upload,
        mock_add_to_cabinets,
        mock_mkdtemp,
        document_config
):
    mock_mkdtemp.return_value = '/tmp/footmp'

    document = Document(*document_config)

    document.process_thread()

    mock_sleep.assert_called_once_with(5)
    mock_scanning.assert_called_once()
    mock_create_pdf.assert_called_once()
    mock_upload.assert_called_once()
    mock_add_to_cabinets.assert_called_once()
    mock_rmtree.assert_called_once_with('/tmp/footmp')

    assert mock_log.info.mock_calls == [
        call('scanning...'),
        call('creating PDF...'),
        call('uploading PDF...'),
        call('adding to cabinets...'),
        call('Done!')
    ]

    assert mock_log.debug.mock_calls == [
        call('creating mayan handler...'),
        call('remove %s...', '/tmp/footmp')
    ]
