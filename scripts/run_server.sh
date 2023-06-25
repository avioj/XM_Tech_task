#!/bin/bash

echo "<============= Running server ===========>"
cd /server/migrations && poetry run alembic stamp head && \
 poetry run alembic revision --autogenerate && poetry run alembic upgrade head
cd /server && poetry run python -m flask run --host=0.0.0.0