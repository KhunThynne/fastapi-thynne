import sys

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typeguard import typechecked

import env

from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        from core.db import init_db

        await init_db()

    except Exception as e:
        print(f"⚠️ Warning: Could not connect to database: {e}")

    yield
    print("FastAPI is shutting down...")
    try:
        from core.db import close_db

        await close_db()
        print("Database connection closed successfully.")
    except Exception as e:
        print(f"⚠️ Warning: Error while disconnecting database: {e}")


app = FastAPI(title=env._env.APP_NAME, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.get("/")
@typechecked
def root() -> dict[str, str]:
    return {"message": "Welcome to Thynne FastAPI"}


if __name__ == "__main__":
    if not env._env.RUNNING_FROM_BAT:
        print("\033[91m\033[1m!" * 50)
        print("\n 🚨 ERROR: Please run via .run.bat only! or read more in README.md \n")
        print("!" * 50 + "\n")
        sys.exit(1)
    import uvicorn

    uvicorn.run(
        "main:app",
        host=env._env.HOST,
        port=env._env.PORT,
        reload=env._env.DEBUG,
    )
