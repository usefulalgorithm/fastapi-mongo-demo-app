from typing import Awaitable, Callable

import beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from test_mongo_project.db.models.user_model import UserModel
from test_mongo_project.settings import settings


async def _setup_db_client(app: FastAPI) -> None:
    client = AsyncIOMotorClient(
        f"mongodb://{settings.mongo_user}:{settings.mongo_password}"
        + f"@{settings.mongo_host}:{settings.mongo_port}/{settings.mongo_database}",
    )
    app.state.client = client
    await beanie.init_beanie(
        database=client[settings.mongo_database],
        document_models=[UserModel],  # type: ignore
    )


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        app.middleware_stack = None
        app.middleware_stack = app.build_middleware_stack()
        await _setup_db_client(app)
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        pass  # noqa: WPS420

    return _shutdown
