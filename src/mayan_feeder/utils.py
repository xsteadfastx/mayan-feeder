"""Some small utils."""

import logging
import os
import webbrowser
from distutils import spawn  # pylint: disable=no-name-in-module
from typing import List

from PIL import Image

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


def is_blank(image_file: str) -> bool:
    """Checks if image is blank.

    Thanks to:
    https://stackoverflow.com/a/18778280
    https://www.splitbrain.org/blog/2014-08/24-paper_backup_2_automation_scripts
    """
    image = Image.open(image_file)
    black_white = image.point(lambda x: 0 if x < 128 else 255, '1')

    black = black_white.histogram()[0]
    white = black_white.histogram()[-1]

    if black / white < 0.005:
        return True

    return False


def selfcheck() -> None:
    """Run all checks and exit if something is missing."""
    if not commands_available(
            [
                'scanimage',
                'tiffcp',
                'tiff2pdf',
            ]
    ):
        LOG.error(
            (
                'Could not find needed commands! '
                'Please install convert and scanimage'
            )
        )
        raise SystemExit(1)
