from fastapi import APIRouter, Response, BackgroundTasks

from app.api.deps import SessionDep
from app.services.auth import AuthorizationService
from app.schemas import MagicLinkRequestSchema

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@auth_router.post("/request")
async def request(
    session: SessionDep,
    data: MagicLinkRequestSchema,
    background_tasks: BackgroundTasks,
):
    await AuthorizationService.request(session, data, background_tasks)
    return {"ok": True, "message": "Link was successfully sent"}


@auth_router.get("/verify")
async def request(
    token: str,
    response: Response,
):
    await AuthorizationService.verify(token, response)
    return {"ok": True, "message": "Successfully logged in"}


@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"ok": True, "message": "Successfully logged out"}
