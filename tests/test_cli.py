# pylint: disable=missing-docstring

import pytest

from mayan_feeder import cli


def test_main_commands_available(monkeypatch):

    monkeypatch.setattr(
        'mayan_feeder.utils.commands_available',
        lambda x: False
    )

    with pytest.raises(SystemExit):
        cli.main([])
