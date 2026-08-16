#!/bin/sh
set -eu

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Add ZEP_API_KEY, then rerun this script."
  exit 1
fi

docker compose build
docker compose up -d redis qdrant
docker compose run --rm app python -m src.smoke
docker compose run --rm app python -m src.seed

echo "Ready. Run: docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded"
