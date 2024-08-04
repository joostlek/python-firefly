"""Asynchronous Python client for Firefly."""

from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp
from aioresponses import aioresponses
import pytest

from vuurvlieg import Vuurvlieg, FireflyError
from tests import load_fixture

from .const import FIREFLY_URL

if TYPE_CHECKING:
    from syrupy import SnapshotAssertion


async def test_putting_in_own_session(
    responses: aioresponses,
) -> None:
    """Test putting in own session."""
    responses.get(
        f"{FIREFLY_URL}/api/v1/about",
        status=200,
        body=load_fixture("about.json"),
    )
    async with aiohttp.ClientSession() as session:
        vuurvlieg = Vuurvlieg(session=session, api_host="https://demo.firefly.io")
        await vuurvlieg.get_about()
        assert vuurvlieg.session is not None
        assert not vuurvlieg.session.closed
        await vuurvlieg.close()
        assert not vuurvlieg.session.closed


async def test_creating_own_session(
    responses: aioresponses,
) -> None:
    """Test creating own session."""
    responses.get(
        f"{FIREFLY_URL}/api/v1/about",
        status=200,
        body=load_fixture("about.json"),
    )
    vuurvlieg = Vuurvlieg(api_host="https://demo.firefly.io", token="XXX")
    await vuurvlieg.get_about()
    assert vuurvlieg.session is not None
    assert not vuurvlieg.session.closed
    await vuurvlieg.close()
    assert vuurvlieg.session.closed


async def test_unexpected_server_response(
    responses: aioresponses,
    firefly_client: Vuurvlieg,
) -> None:
    """Test handling unexpected response."""
    responses.get(
        f"{FIREFLY_URL}/api/v1/about",
        status=200,
        headers={"Content-Type": "plain/text"},
        body="Yes",
    )
    with pytest.raises(FireflyError):
        assert await firefly_client.get_about()


async def test_about(
    responses: aioresponses,
    firefly_client: Vuurvlieg,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving about."""
    responses.get(
        f"{FIREFLY_URL}/api/v1/about",
        status=200,
        body=load_fixture("about.json"),
    )
    assert await firefly_client.get_about() == snapshot
