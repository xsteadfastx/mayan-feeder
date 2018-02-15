"""Forms."""

import logging
from typing import List, Tuple, Union

from flask_wtf import FlaskForm
from wtforms.fields import SelectMultipleField, SubmitField

from mayan_feeder import config, mayan

LOG = logging.getLogger(__name__)


def create_cabinets() -> Union[List[Tuple[str, str]], None]:
    """Create cabinet fields for form."""
    config_dict = config.get()
    if config_dict:

        m_handler = mayan.MayanHandler(
            config_dict['mayan']['url'],
            config_dict['mayan']['username'],
            config_dict['mayan']['password']
        )

        return [
            (str(i['id']), i['label'])
            for i in m_handler.cabinets['results']
        ]

    return None


class DocumentForm(FlaskForm):
    """Document upload form."""
    cabinets = SelectMultipleField('Select cabinets')
    submit = SubmitField('Scan...')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cabinets.choices = create_cabinets()
