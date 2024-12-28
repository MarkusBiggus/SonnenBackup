"""Common fixtures for the SonnenBackup tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
#        "homeassistant.components.sonnenbackup.async_setup_entry", return_value=True
        "custom_components.sonnenbackup.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        yield mock_setup_entry

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield