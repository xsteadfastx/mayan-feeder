# pylint: disable=missing-docstring

from datetime import datetime
from unittest.mock import call, patch, sentinel

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
    assert document.pdf_filename == '20171208000000.pdf'
    assert document.tempdir == '/tmp/footmp'
    assert document.pdf_file_path == '/tmp/footmp/20171208000000.pdf'


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
        call('removing blanks...'),
        call('creating PDF...'),
        call('uploading PDF...'),
        call('adding to cabinets...'),
        call('Done!')
    ]

    assert mock_log.debug.mock_calls == [
        call('creating mayan handler...'),
        call('remove %s...', '/tmp/footmp')
    ]


@patch('mayan_feeder.document.utils.ChDir', autospec=True)
@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
@patch('mayan_feeder.document.subprocess', autospec=True)
@patch('mayan_feeder.document.LOG', autospec=True)
def test_scanning(
        mock_log,
        mock_subprocess,
        mock_mkdtemp,
        mock_chdir,
        document_config
):
    mock_mkdtemp.return_value = '/tmp/footmp'

    mock_subprocess.Popen.return_value.\
        __enter__.return_value.\
        stdout.read.return_value.\
        decode.return_value = 'foo'

    document = Document(*document_config)
    document.scanning()

    mock_subprocess.Popen.assert_called_with(
        [
            'scanimage',
            '-y', '279.4',
            '-x', '215.9',
            '--batch',
            '--format=tiff',
            '--mode', 'Gray',
            '--resolution', '300',
            '--source', 'ADF Duplex'
        ],
        stdout=mock_subprocess.PIPE,
        stderr=mock_subprocess.STDOUT
    )

    assert mock_log.debug.mock_calls == [
        call('creating mayan handler...'),
        call('scanning to %s', '/tmp/footmp'),
        call('%s', 'foo')
    ]

    mock_chdir.assert_called_with('/tmp/footmp')


@patch('mayan_feeder.document.utils.ChDir')
@patch('mayan_feeder.document.LOG')
def test_scanning_exception(mock_log, mock_chdir, document_config):
    mock_chdir.side_effect = IndexError(sentinel.error)

    document = Document(*document_config)
    document.scanning()

    mock_log.exception.assert_called_with(str(sentinel.error))


@patch('mayan_feeder.document.datetime', autospec=True)
@patch('mayan_feeder.document.subprocess', autospec=True)
@patch('mayan_feeder.document.utils.ChDir')
@patch('mayan_feeder.document.LOG')
@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
@patch('mayan_feeder.document.os', autospec=True)
def test_create_pdf(
        mock_os,
        mock_mkdtemp,
        mock_log,
        mock_chdir,
        mock_subprocess,
        mock_datetime,
        document_config
):
    mock_mkdtemp.return_value = sentinel.tmpdir

    mock_os.path.isfile.return_value = True

    mock_os.listdir.return_value = ['1.tiff']

    mock_datetime.now.return_value = datetime(2017, 12, 8, 0, 0, 0, 0)

    document = Document(*document_config)
    document.create_pdf()

    mock_chdir.assert_called_with(str(sentinel.tmpdir))

    stdout = mock_subprocess.Popen.return_value.__enter__.return_value.\
        stdout.read.return_value.decode.return_value

    assert mock_log.mock_calls == [
        call.debug('creating mayan handler...'),
        call.debug('found: \n%s', '1.tiff'),
        call.debug('command list: %s', ['tiffcp', '1.tiff', 'complete.tif']),
        call.debug('%s', stdout),
        call.debug('%s', stdout),
    ]

    assert call(
        ['tiffcp', '1.tiff', 'complete.tif'],
        stdout=mock_subprocess.PIPE,
        stderr=mock_subprocess.STDOUT
    ) in mock_subprocess.mock_calls

    assert call(
        ['tiff2pdf', '-o', '20171208000000.pdf', 'complete.tif'],
        stdout=mock_subprocess.PIPE,
        stderr=mock_subprocess.STDOUT
    ) in mock_subprocess.mock_calls


# pylint: disable=invalid-name
@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
@patch('mayan_feeder.document.LOG', autospec=True)
@patch('mayan_feeder.document.os', autospec=True)
def test_create_pdf_not_enough_pages(
        mock_os,
        mock_log,
        mock_mkdtemp,
        document_config
):
    mock_mkdtemp.return_value = sentinel.tmpdir

    mock_os.listdir.return_value = []

    document = Document(*document_config)
    document.create_pdf()

    mock_log.error.assert_called_with('not enough pages')


@patch('mayan_feeder.document.LOG', autospec=True)
@patch('mayan_feeder.document.os', autospec=True)
def test_create_pdf_exception(mock_os, mock_log, document_config):
    mock_os.listdir.side_effect = IndexError(sentinel.error)

    document = Document(*document_config)
    document.create_pdf()

    mock_log.exception.assert_called_with(str(sentinel.error))


@patch('mayan_feeder.document.datetime', autospec=True)
@patch('mayan_feeder.document.os', autospec=True)
@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
@patch('mayan_feeder.document.LOG')
def test_pages(
        mock_log,
        mock_mkdtemp,
        mock_os,
        mock_datetime,
        document_config
):
    mock_mkdtemp.return_value = sentinel.tmpdir

    mock_os.path.isfile.return_value = True

    mock_os.listdir.return_value = ['1.tiff', '2.tiff']

    mock_datetime.now.return_value = datetime(2018, 1, 15, 0, 0, 0, 0)

    document = Document(*document_config)

    assert document.pages == ['1.tiff', '2.tiff']

    assert mock_log.debug.call_args_list == [
        call('creating mayan handler...'),
        call('found: \n%s', '1.tiff\n2.tiff')
    ]


@patch('mayan_feeder.document.Document.pages')
@patch('mayan_feeder.document.os.remove')
@patch('mayan_feeder.document.utils.is_blank')
@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
def test_remove_blanks(
        mock_mkdtemp,
        mock_is_blank,
        mock_remove,
        mock_pages,  # pylint: disable=unused-argument
        document_config,
):
    mock_mkdtemp.return_value = sentinel.tmpdir

    mock_is_blank.return_value = True

    document = Document(*document_config)

    document.pages = ['1.tiff']

    document.remove_blanks()

    mock_remove.assert_called_once_with('1.tiff')


@patch('mayan_feeder.document.LOG')
@patch('mayan_feeder.document.Document.pages')
@patch('mayan_feeder.document.utils.is_blank')
@patch('mayan_feeder.document.tempfile.mkdtemp', autospec=True)
def test_remove_blanks_exception(
        mock_mkdtemp,
        mock_is_blank,
        mock_pages,  # pylint: disable=unused-argument
        mock_log,
        document_config
):
    mock_mkdtemp.return_value = sentinel.tmpdir

    mock_is_blank.side_effect = IndexError('foo')

    document = Document(*document_config)

    document.pages = ['1.tiff']

    document.remove_blanks()

    mock_log.exception.assert_called_once_with('foo')
