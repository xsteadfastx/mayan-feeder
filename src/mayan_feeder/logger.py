"""Logging helpers."""

from logging import Handler, LogRecord
from typing import Dict

from mayan_feeder import web


class SocketIOHandler(Handler):
    """Sends log messages over socket.io."""
    def _colorize_it(self, record: LogRecord) -> Dict[str, str]:
        """Sets css class for log message level."""
        if record.levelname == 'INFO':
            css_class = 'success'
        elif record.levelname == 'DEBUG':
            css_class = 'info'
        elif record.levelname == 'WARNING':
            css_class = 'warning'
        elif record.levelname == 'CRITICAL':
            css_class = 'danger'
        elif record.levelname == 'ERROR':
            css_class = 'danger'
        elif record.levelname == 'EXCEPTION':
            css_class = 'danger'
        else:
            css_class = 'muted'

        log_entry = self.format(record)

        return {'class': css_class, 'msg': log_entry}

    def emit(self, record: LogRecord) -> None:
        if record.name.startswith('mayan_feeder'):

            log_entry = self._colorize_it(record)

            web.SOCKETIO.emit(
                'my response',
                log_entry,
                namespace='/feeder',
                json=True
            )
