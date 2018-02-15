"""Prompt."""

from prompt_toolkit.shortcuts.dialogs import message_dialog, button_dialog

message_dialog(
    title='Example dialog window',
    text='Do you want to continue?\nPress ENTER to quit.')
