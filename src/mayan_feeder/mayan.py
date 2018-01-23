"""Interaction with the Mayan API."""
import logging
from typing import BinaryIO, Dict, Union
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

LOG = logging.getLogger(__name__)


class CouldNotConnect(BaseException):
    """Exception raises if cant connect to MayanEDMS."""
    pass


class MayanHandler(object):
    """Mayan Handler."""

    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password

    def create_url(self, endpoint: str) -> str:
        """Joins Mayan url with endpoint."""
        return urljoin(self.url, endpoint)

    def r_get(self, endpoint: str) -> Dict:  # pragma: no cover
        """GET request on Mayan API."""
        url = self.create_url(endpoint)
        LOG.debug('GET on url: %s', url)

        response = requests.get(
            url,
            auth=HTTPBasicAuth(
                self.username,
                self.password
            )
        )

        data = response.json()

        LOG.debug('got response: %s', data)

        return data

    def r_post(
            self,
            endpoint: str,
            data: Dict,
            files: Union[None, Dict[str, BinaryIO]]
    ) -> Dict:  # pragma: no cover
        """POST request on Mayan API."""

        url = self.create_url(endpoint)
        LOG.debug('POST to url: %s', url)

        response = requests.post(
            url,
            auth=HTTPBasicAuth(
                self.username,
                self.password
            ),
            data=data,
            files=files
        )

        response_data = response.json()

        LOG.debug('got response: %s', response_data)

        return response_data

    def cabinets(self) -> Dict:  # pragma: no cover
        """Getting all cabinets from API."""
        LOG.debug('get cabinets from api...')

        data = self.r_get('/api/cabinets/cabinets')

        return data

    def add_to_cabinet(
            self,
            cabinet_id: str,
            document_id: int
    ) -> None:  # pragma: no cover
        "Add document to cabinet."
        LOG.debug(
            'add to document %s to cabinet %s',
            document_id, cabinet_id
        )

        self.r_post(
            f'/api/cabinets/cabinets/{cabinet_id}/documents/',
            data={
                'pk': cabinet_id,
                'documents_pk_list': document_id
            },
            files=None
        )

    def upload(
            self,
            pdf_file_path: str
    ) -> Dict[str, Union[int, str]]:  # pragma: no cover
        """Upload PDF file to Mayan API."""

        with open(pdf_file_path, 'rb') as pdf_file:
            response = self.r_post(
                '/api/documents/documents/',
                {
                    'document_type': 1,
                },
                {
                    'file': pdf_file
                }
            )

        return response

    @property
    def is_available(self) -> None:
        """Checking mayan availability."""
        LOG.info('checking if mayan is available...')
        try:
            data = self.r_get('/api/motd/messages/')
            # pylint: disable=expression-not-assigned,pointless-statement
            data['results']

        except BaseException:
            raise CouldNotConnect(f'Could not connect to {self.url}')
