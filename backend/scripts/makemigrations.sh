#!/bin/bash
set -x

docker exec backend alembic revision --autogenerate -m "$1"