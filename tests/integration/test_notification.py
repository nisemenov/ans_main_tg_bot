from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.conftest import test_settings

if TYPE_CHECKING:
    from httpx import AsyncClient


pytestmark = pytest.mark.anyio

url: str = test_settings.API_STR + '/notifications'


async def test_notification_create(client: AsyncClient) -> None:
    response = await client.post(
        url=url, 
        json={
            'service': 'wisdom', 
            'message': 'test_message'
        }
    )

    assert response.status_code == 201
