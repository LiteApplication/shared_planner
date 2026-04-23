#!/bin/sh
set -e

uv run init_settings

exec uv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
    shared_planner.api:app --bind 0.0.0.0:8000
