"""Document class."""

import logging
import os
import subprocess
import tempfile
from datetime import datetime
from shutil import rmtree
from threading import Thread
from time import sleep
from typing import List

import attr

from mayan_feeder import mayan, utils

LOG = logging.getLogger(__name__)


@attr.s
class Document(object):
    """Document object."""

    url: str = attr.ib()
    username: str = attr.ib()
    password: str = attr.ib()

    cabinets: List[str] = attr.ib()

    now: datetime = attr.ib(init=False)

    tempdir: str = attr.ib(init=False)

    pdf_filename: str = attr.ib(init=False)
    pdf_file_path: str = attr.ib(init=False)
    document_id: int = attr.ib(init=False)

    mayan_handler: mayan.MayanHandler = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        # time
        self.now = datetime.now()

        # filename
        self.pdf_filename = '{}.pdf'.format(self.now.strftime('%Y%m%d%H%M%S'))
        # tempdir
        self.tempdir = str(tempfile.mkdtemp())

        # pdf fullpath
        self.pdf_file_path = os.path.join(self.tempdir, self.pdf_filename)

        # mayan
        LOG.debug('creating mayan handler...')
        self.mayan_handler = mayan.MayanHandler(
            self.url,
            self.username,
            self.password
        )

    def upload(self) -> None:
        """Upload to Mayan EDMS."""
        try:
            response = self.mayan_handler.upload(self.pdf_file_path)
            self.document_id = int(response['id'])
        except BaseException as exception:
            LOG.exception(str(exception))

    def add_to_cabinets(self) -> None:
        """Add PDF to cabinets."""
        try:
            for cabinet in iter(self.cabinets):
                LOG.debug('adding to cabinet %s...', cabinet)
                self.mayan_handler.add_to_cabinet(cabinet, self.document_id)
        except BaseException as exception:
            LOG.exception(str(exception))

    def process(self) -> None:
        """Scan document."""
        LOG.debug('starting thread...')
        Thread(target=self.process_thread).start()

    def process_thread(self) -> None:
        """Main process function."""
        sleep(5)

        LOG.info('scanning...')
        self.scanning()

        LOG.info('creating PDF...')
        self.create_pdf()

        LOG.info('uploading PDF...')
        self.upload()

        LOG.info('adding to cabinets...')
        self.add_to_cabinets()

        LOG.debug('remove %s...', self.tempdir)
        rmtree(self.tempdir)

        LOG.info('Done!')

    def scanning(self) -> None:
        """Scan in a seperated thread."""
        command: List[str] = [
            'scanimage',
            '-y', '279.4',
            '-x', '215.9',
            '--batch',
            '--format=tiff',
            '--mode', 'Gray',
            '--resolution', '300',
            '--source', 'ADF Duplex',
        ]

        try:
            LOG.debug('scanning to %s', self.tempdir)
            with utils.ChDir(self.tempdir):

                with subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                ) as proc:

                    LOG.debug('%s', proc.stdout.read().decode('utf-8'))

        except BaseException as exception:
            LOG.exception(str(exception))

    def create_pdf(self) -> None:
        """Creating pdf from tiff files."""
        try:

            pages = [
                str(i)
                for i in os.listdir(self.tempdir)
                if os.path.isfile(
                    os.path.join(
                        self.tempdir,
                        i
                    )
                )
            ]
            LOG.debug('found: \n%s', '\n'.join(pages))

            if len(pages) >= 1:

                with utils.ChDir(self.tempdir):

                    command = [
                        'tiffcp'
                    ]
                    command.extend(sorted(pages))
                    command.append('complete.tif')
                    LOG.debug('command list: %s', command)

                    with subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT
                    ) as proc:

                        LOG.debug('%s', proc.stdout.read().decode('utf-8'))

                    with subprocess.Popen(
                        [
                            'tiff2pdf',
                            '-o', self.pdf_filename,
                            'complete.tif'
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT
                    ) as proc:

                        LOG.debug('%s', proc.stdout.read().decode('utf-8'))

            else:
                LOG.error('not enough pages')

        except BaseException as exception:
            LOG.exception(str(exception))
