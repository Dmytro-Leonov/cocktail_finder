#!/bin/bash
set -x

docker exec backend ruff check ./app