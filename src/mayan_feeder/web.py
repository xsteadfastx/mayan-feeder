"""Web GUI."""

import logging

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

LOG = logging.getLogger(__name__)

APP = Flask(__name__)

Bootstrap(APP)
SOCKETIO = SocketIO(APP)


@APP.route('/', methods=('GET', 'POST'))
def root():
    """root route."""
    from mayan_feeder import config, forms, document

    LOG.info('Getting root route...')
    form = forms.DocumentForm(csrf_enabled=False)

    if form.validate_on_submit():
        settings = config.get()
        doc = document.Document(
            settings['mayan']['url'],
            settings['mayan']['username'],
            settings['mayan']['password']
        )
        doc.process()

    return render_template('index.html', form=form)


# @APP.route('/foo')
# def foo():
#     LOG.info('IIINNNFFFOOOOO')
#     LOG.debug('DDEEEBBBUUUUGGGGG')
#     LOG.error('EERRROOORRRR')
#     return 'foo'
