from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import core_config
from app.db.session_manager import sessionmanager


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title=core_config.PROJECT_NAME,
    openapi_url=f"{core_config.API_PREFIX}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if core_config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in core_config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=core_config.API_PREFIX)
