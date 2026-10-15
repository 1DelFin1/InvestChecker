from typing import Annotated

from fastapi import APIRouter, Response, Depends

from app.api.deps import SessionDep
from app.api.request_form import OAuth2EmailRequestForm
from app.services.auth import AuthorizationService

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@auth_router.post("/login")
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2EmailRequestForm, Depends()],
    response: Response,
):
    await AuthorizationService.login(session, form_data, response)
    return {"ok": True, "message": "Successfully logged in"}


@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie("token")
    return {"ok": True, "message": "Successfully logged out"}
