"""Console interface."""

import logging

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts.dialogs import button_dialog, radiolist_dialog

from mayan_feeder import config, document, mayan

LOG = logging.getLogger(__name__)


class Console(object):
    """Console object."""
    def __init__(self):
        self._config = config.get()
        self._mayan_handler = mayan.MayanHandler(
            self._config['mayan']['url'],
            self._config['mayan']['username'],
            self._config['mayan']['password'],
        )
        self._cabinet_data = self._mayan_handler.cabinets['results']
        self._cabinet_dict = {}
        for cabinet in self._cabinet_data:
            self._cabinet_dict[cabinet['id']] = cabinet['label']
        self._cabinets_choosen = []
        self._cabinets_available = [
            (i['id'], i['label'])
            for i in self._cabinet_data
        ]

    def dialog_choose_cabinets(self) -> str:
        """Dialog to choose cabinet from a list."""
        cabinet = radiolist_dialog(
            title='Choose cabinet',
            values=self._cabinets_available
        )

        self._cabinets_choosen.append(cabinet)

        return 'main'

    def dialog_main(self) -> str:
        """Overview main dialog."""
        if self._cabinets_choosen:
            cabinets_text = [
                '<strong>Cabinets</strong>:'
            ]
            cabinets_text.extend(
                [
                    self._cabinet_dict[i]
                    for i in set(self._cabinets_choosen)
                ]
            )
            text = HTML('\n'.join(cabinets_text))
        else:
            text = ''
        dialog = button_dialog(
            title='Mayan-Feeder',
            text=text,
            buttons=[
                ('Add cabinet', 'cabinets'),
                ('Scan', 'scan'),
                ('Reset', 'reset'),
                ('Exit', 'exit')
            ]
        )

        return dialog

    def dialog_scan(self) -> str:
        """Scan dialog."""
        doc = document.Document(
            self._config['mayan']['url'],
            self._config['mayan']['username'],
            self._config['mayan']['password'],
            self._cabinets_choosen
        )

        doc.process_thread()

        return 'main'

    def dialog_reset(self) -> str:
        """Resets cabinets."""
        self._cabinets_choosen = []

        return 'main'

    def run(self) -> None:
        """Runs the dialogs."""
        value = 'main'
        while value != 'exit':
            if value == 'main':
                value = self.dialog_main()
            elif value == 'cabinets':
                value = self.dialog_choose_cabinets()
            elif value == 'scan':
                value = self.dialog_scan()
            elif value == 'reset':
                value = self.dialog_reset()


Console().run()
