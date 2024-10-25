import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from shared_planner.api.auth import router as auth_router
from shared_planner.api.users import router as users_router
from shared_planner.api.shops import router as shops_router, timerange_router
from shared_planner.api.reservations import router as reservations_router
from shared_planner.api.settings import router as settings_router
from shared_planner.api.notifications import router as notifications_router
from pathlib import Path

app = FastAPI(swagger_ui_parameters={"persistAuthorization": True}, root_path="/api")

BASE_DIR = Path(__file__).resolve().parent.parent.parent / "web" / "dist"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(shops_router)
app.include_router(timerange_router)
app.include_router(reservations_router)
app.include_router(settings_router)
app.include_router(notifications_router)


def sanitize_path(path: str) -> str:
    return os.path.normpath(path).replace("..", "")


@app.get("/{rest_of_path:path}")
def serve_my_app(rest_of_path: str):
    rest_of_path = sanitize_path(rest_of_path)

    if rest_of_path == "":
        return FileResponse(BASE_DIR / "index.html")
    if (BASE_DIR / rest_of_path).exists():
        return FileResponse(BASE_DIR / rest_of_path)
    return FileResponse(BASE_DIR / "index.html")
