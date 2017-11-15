"""Config"""

# pylint: disable=no-member

import logging
import sys
from pathlib import Path
from typing import Dict, Union

import yaml
from click import echo

LOG = logging.getLogger(__name__)


def get() -> Union[Dict[str, Dict[str, str]], None]:
    """Get config."""
    config_file = Path.home().joinpath('.mayanfeeder.yaml')

    if not config_file.exists():
        echo('No configfile found!')
        sys.exit(1)

    LOG.debug('Parsing config file...')
    with config_file.open() as opened_config:
        settings = yaml.load(opened_config.read())
    LOG.debug('Parsed config: %s', settings)

    if 'mayan' not in settings.keys():
        echo('No mayan section in config!')
        sys.exit(1)

    if not all(
            i in settings['mayan'].keys()
            for i in ['url', 'username', 'password']
    ):
        echo('Missing url, username or password in mayan settings!')
        sys.exit(1)

    return settings
