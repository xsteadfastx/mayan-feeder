"""Some small utils."""

import logging
import os
import webbrowser
from distutils import spawn  # pylint: disable=no-name-in-module
from typing import List

LOG = logging.getLogger(__name__)


def open_browser() -> None:  # pragma: no cover
    """Open app in browser."""
    LOG.info('Open browser...')
    webbrowser.open('http://127.0.0.1:5000')


# pylint: disable=too-few-public-methods
class ChDir(object):
    """Contextmanager to temporary change dir."""

    def __init__(self, new_dir: str) -> None:
        self.old_dir: str = os.getcwd()
        self.new_dir: str = new_dir

    def __enter__(self):
        LOG.debug('enter %s...', self.new_dir)
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        LOG.debug('enter %s again...', self.old_dir)
        os.chdir(self.old_dir)


def commands_available(commands: List[str]) -> bool:
    """Check if needed commands are available."""
    return all([spawn.find_executable(command) for command in commands])
