from typing import Any, Optional, cast

from fastapi import HTTPException, status
from fastapi.openapi.models import OAuthFlows
from fastapi.requests import Request
from fastapi.security import OAuth2


class OAuth2CookieJWT(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        description: str = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes}))
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        access_token = request.cookies.get("access_token")

        if not access_token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None

        return access_token
