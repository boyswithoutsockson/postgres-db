#!/bin/bash
# Script to delete only the postgres-data volume and reinitialize the postgres container

set -e

docker compose -p eduri_devcontainer -f .devcontainer/docker-compose.yml stop db
docker compose -p eduri_devcontainer -f .devcontainer/docker-compose.yml down db -v
docker compose -p eduri_devcontainer -f .devcontainer/docker-compose.yml build db
docker compose -p eduri_devcontainer -f .devcontainer/docker-compose.yml up -d db

echo "Postgres container reinitialized. Init scripts have been re-run."
