from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import PermissionDenied
from app.db.dependencies import DBSessionDep
from app.modules.auth.dependencies import CurrentUserByRefreshToken
from app.modules.auth.exceptions import InvalidCredentials
from app.modules.auth.security import check_password
from app.modules.auth.services import (
    create_access_token,
    create_refresh_token,
    get_user_by_username_or_email,
    set_access_token_cookie,
    set_refresh_token_cookie,
)

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
) -> None:
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

    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)

    set_access_token_cookie(response, access_token=access_token)
    set_refresh_token_cookie(response, refresh_token=refresh_token)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Logout",
)
async def logout(response: Response) -> None:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    description="Refresh access token",
)
async def refresh(response: Response, user: CurrentUserByRefreshToken) -> None:
    access_token = create_access_token(user=user)
    set_access_token_cookie(response, access_token=access_token)
