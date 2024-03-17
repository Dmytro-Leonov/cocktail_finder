from typing import Annotated

from fastapi import Depends

from app.modules.auth.services import (
    get_current_admin,
    get_current_user,
    get_current_user_by_refresh_token,
    get_current_user_optional,
)
from app.modules.user.models import User

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]
CurrentUserAdmin = Annotated[User, Depends(get_current_admin)]
CurrentUserByRefreshToken = Annotated[User, Depends(get_current_user_by_refresh_token)]
