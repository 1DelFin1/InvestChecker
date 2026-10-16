from fastapi import APIRouter, Depends

from app.api.deps import ensure_user_access
from app.services import PODService

pods_router = APIRouter(prefix="/api/v1/pods", tags=["pods"])


@pods_router.get("")
async def get_pods():
    user = await PODService.get_egrkn()
    return user

