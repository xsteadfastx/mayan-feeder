"""Cli."""

import logging
import threading

import click

from mayan_feeder import utils

LOG = logging.getLogger(__name__)


@click.group()
@click.option(
    '-v', '--verbose',
    count=True,
    help='Can be used multiply times.'
)
@click.version_option()
def cli(verbose: int) -> None:
    """Feed documents into MayanEDMS."""
    # setting up logging
    logging.basicConfig()

    if verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


@cli.command()
def browser() -> None:
    """Opens browser to feed."""

    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
    logging.getLogger('socketio').setLevel(logging.CRITICAL)
    logging.getLogger('engineio').setLevel(logging.CRITICAL)

    from mayan_feeder import logger, web

    logging.getLogger().addHandler(logger.SocketIOHandler())

    # run selfchecks
    utils.selfcheck()

    LOG.debug('Adding timer thread to start Browser...')
    threading.Timer(
        1.25,
        utils.open_browser
    ).start()

    LOG.info('Starting the feeder...')

    web.SOCKETIO.run(web.APP)


@cli.command()
def console() -> None:
    """Opens console to feed."""
    click.echo('foo')
