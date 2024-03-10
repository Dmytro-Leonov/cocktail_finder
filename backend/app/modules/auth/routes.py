from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import PermissionDenied
from app.db.dependencies import DBSessionDep
from app.modules.auth.config import auth_config
from app.modules.auth.exceptions import InvalidCredentials
from app.modules.auth.security import check_password
from app.modules.auth.services import create_jwt, get_user_by_username_or_email

auth_router = router = APIRouter()


@router.post(
    "/login/username-or-email",
    status_code=status.HTTP_200_OK,
    description="Login with email and password",
)
async def login_email_and_password(
    session: DBSessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    user = await get_user_by_username_or_email(
        session, username_or_email=form_data.username
    )

    if user is None:
        raise InvalidCredentials()
    if not check_password(
        plain_password=form_data.password, hashed_password=user.hashed_password
    ):
        raise InvalidCredentials()
    if not user.is_active:
        raise PermissionDenied()

    access_token = create_jwt(
        data={"user_id": user.id},
        expires_delta=timedelta(seconds=auth_config.ACCESS_TOKEN_EXPIRE_SECONDS),
    )
    refresh_token = create_jwt(
        data={"user_id": user.id},
        expires_delta=timedelta(seconds=auth_config.REFRESH_TOKEN_EXPIRE_SECONDS),
    )

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=True,
        max_age=auth_config.ACCESS_TOKEN_EXPIRE_SECONDS,
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        max_age=auth_config.REFRESH_TOKEN_EXPIRE_SECONDS,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Logout",
)
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
