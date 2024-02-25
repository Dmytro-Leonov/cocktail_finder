#!/bin/bash
set -x

docker exec -it backend sh -c "ruff check ./app --fix --show-fixes && ruff format ./app"