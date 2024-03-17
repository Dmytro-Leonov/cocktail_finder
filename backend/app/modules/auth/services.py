from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, Request, Response
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import core_config
from app.core.exceptions import NotAuthenticated
from app.db.dependencies import DBSessionDep
from app.db.models import User
from app.modules.auth.config import auth_config
from app.modules.auth.exceptions import (
    AuthorizationFailed,
    InvalidCredentials,
    InvalidToken,
)
from app.modules.auth.oauth2 import OAuth2CookieJWT

oauth2_scheme = OAuth2CookieJWT(
    tokenUrl="auth/login/username-or-email", auto_error=False
)

AccessTokenDep = Annotated[Optional[str], Depends(oauth2_scheme)]


async def get_user_by_id(session: AsyncSession, *, user_id: int) -> Optional[User]:
    query = select(User).where(User.id == user_id)
    user = await session.scalar(query)

    return user


async def get_user_by_username_or_email(
    session: AsyncSession, *, username_or_email: str
) -> Optional[User]:
    query = select(User).where(
        (User.email == username_or_email) | (User.username == username_or_email)
    )
    user = (await session.scalars(query)).first()

    return user


async def get_current_user(
    session: DBSessionDep,
    access_token: AccessTokenDep,
) -> User:
    if access_token is None:
        raise NotAuthenticated()

    try:
        payload = jwt.decode(
            access_token,
            core_config.SECRET_KEY,
            algorithms=auth_config.HASH_ALGORITHM,
        )
        user_id: Optional[int] = payload.get("user_id")
        if user_id is None:
            raise InvalidToken()
    except JWTError:
        raise InvalidToken()

    user = await get_user_by_id(session, user_id=user_id)

    if user is None:
        raise InvalidCredentials()

    if not user.is_active:
        raise AuthorizationFailed()

    return user


async def get_current_user_optional(
    session: DBSessionDep,
    access_token: AccessTokenDep,
) -> Optional[User]:
    if access_token:
        return await get_current_user(session, access_token=access_token)

    return None


async def get_current_admin(
    session: DBSessionDep,
    access_token: AccessTokenDep,
) -> User:
    if access_token is None:
        raise NotAuthenticated()

    user = await get_current_user(session, access_token=access_token)

    if not user.is_superuser:
        raise AuthorizationFailed()

    return user


def create_jwt(*, data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    created_jwt = jwt.encode(
        to_encode, core_config.SECRET_KEY, algorithm=auth_config.HASH_ALGORITHM
    )

    return created_jwt


def create_access_token(*, user: User) -> str:
    return create_jwt(
        data={"user_id": user.id},
        expires_delta=timedelta(seconds=auth_config.ACCESS_TOKEN_EXPIRE_SECONDS),
    )


def create_refresh_token(*, user: User) -> str:
    return create_jwt(
        data={"user_id": user.id},
        expires_delta=timedelta(seconds=auth_config.REFRESH_TOKEN_EXPIRE_SECONDS),
    )


def set_access_token_cookie(response: Response, *, access_token: str) -> None:
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=True,
        max_age=auth_config.ACCESS_TOKEN_EXPIRE_SECONDS,
    )


def set_refresh_token_cookie(response: Response, *, refresh_token: str) -> None:
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        max_age=auth_config.REFRESH_TOKEN_EXPIRE_SECONDS,
    )


async def get_current_user_by_refresh_token(
    session: DBSessionDep, *, request: Request
) -> Optional[str]:
    refresh_token = request.cookies.get("refresh_token")

    return await get_current_user(session, access_token=refresh_token)
