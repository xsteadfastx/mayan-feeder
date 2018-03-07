"""Cli."""

import logging
import sys
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

    from mayan_feeder import logger, web, config, mayan

    logging.getLogger().addHandler(logger.SocketIOHandler())

    # selfcheck if all needed commands are available
    utils.selfcheck()

    config_dict = config.get()
    try:
        mayan.MayanHandler(
            config_dict['mayan']['url'],
            config_dict['mayan']['username'],
            config_dict['mayan']['password']
        ).is_available
    except mayan.CouldNotConnect:
        LOG.error('Could not connect to MayanEDMS')
        sys.exit(1)

    LOG.debug('Adding timer thread to start Browser...')
    threading.Timer(
        1.25,
        utils.open_browser
    ).start()

    LOG.info('Starting the feeder...')

    web.SOCKETIO.run(web.APP)


@cli.command()
def console():
    """Opens console to feed."""
    pass
