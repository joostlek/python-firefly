"""Asynchronous Python client for Firefly."""

from typing import AsyncGenerator, Generator

import aiohttp
from aioresponses import aioresponses
import pytest

from syrupy import SnapshotAssertion

from vuurvlieg import Vuurvlieg

from tests.syrupy import FireflySnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Firefly extension."""
    return snapshot.use_extension(FireflySnapshotExtension)


@pytest.fixture(name="firefly_client")
async def client() -> AsyncGenerator[Vuurvlieg, None]:
    """Return a Firefly client."""
    async with aiohttp.ClientSession() as session, Vuurvlieg(
        "https://demo.firefly.io",
        session=session,
    ) as firefly_client:
        yield firefly_client


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
