#!/bin/bash
set -x

docker exec backend alembic downgrade "$1"