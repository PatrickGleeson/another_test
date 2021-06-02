from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """
    Primarily for testing that the infrastructure and testing apparatuses are setup correctly.
    """

    response = await client.get(f"/health-check")
    assert response.status_code == 200

    data = response.json()
    assert data["service"]["status"] == "healthy"
    assert data["service"]["error"] is None
    assert data["database"]["status"] == "healthy"
    assert data["database"]["error"] is None
