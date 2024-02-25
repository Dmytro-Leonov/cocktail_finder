#!/bin/bash
set -x

docker exec backend alembic upgrade head