"""Cli."""

import logging
import threading

import click

LOG = logging.getLogger(__name__)


@click.command()
@click.option(
    '-v', '--verbose',
    count=True,
    help='Can be used multiply times.'
)
@click.version_option()
def main(verbose: int) -> None:
    """Feed documents into MayanEDMS."""

    # setting up logging
    logging.basicConfig()

    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
    logging.getLogger('socketio').setLevel(logging.CRITICAL)
    logging.getLogger('engineio').setLevel(logging.CRITICAL)

    if verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    from mayan_feeder import logger, utils, web

    logging.getLogger().addHandler(logger.SocketIOHandler())

    LOG.debug('Adding timer thread to start Browser...')
    threading.Timer(
        1.25,
        utils.open_browser
    ).start()

    LOG.info('Starting the feeder...')

    web.SOCKETIO.run(web.APP)
