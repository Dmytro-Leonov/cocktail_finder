from typing import Annotated, Optional

from fastapi import Depends

from app.modules.auth.services import (
    get_current_admin,
    get_current_user,
    get_current_user_optional,
)
from app.modules.user.models import User

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserOptional = Annotated[Optional[User], Depends(get_current_user_optional)]
CurrentUserAdmin = Annotated[User, Depends(get_current_admin)]
