#!/bin/sh -e
set -x

docker exec backend alembic downgrade "$1"