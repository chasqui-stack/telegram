"""Test config: provide required env + keep the Bot off the network.

Settings() reads TELEGRAM_* at import time, and the app lifespan calls
Bot.initialize()/shutdown() (which would hit api.telegram.org). Tests stub
both so nothing leaves the process.
"""

import os

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token")
os.environ.setdefault("TELEGRAM_WEBHOOK_SECRET", "test-secret")

import pytest  # noqa: E402
from telegram import Bot  # noqa: E402


@pytest.fixture(autouse=True)
def _offline_bot(monkeypatch):
    async def _noop(self, *args, **kwargs):
        return None

    monkeypatch.setattr(Bot, "initialize", _noop)
    monkeypatch.setattr(Bot, "shutdown", _noop)
