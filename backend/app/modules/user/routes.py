from fastapi import APIRouter, status

from app.db.models import User
from app.modules.auth.dependencies import CurrentUser
from app.modules.user.schemas import UserMeOut

user_router = router = APIRouter()


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserMeOut,
    description="Get current user",
)
async def get_me(user: CurrentUser) -> User:
    return user
