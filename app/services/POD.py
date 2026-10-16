from httpx import AsyncClient

from app.core.config import settings


class PODService:
    @classmethod
    async def get_egrkn(cls):
        async with AsyncClient() as client:
            response = await client.get(
                f"{settings.integration.POD_URL}/egrkn",
                headers={"X-API-KEY": settings.integration.API_KEY_POD},
            )

        return response.json()
