from fastapi import APIRouter

from app.modules.auth.routes import auth_router
from app.modules.user.routes import user_router

api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["user"])
