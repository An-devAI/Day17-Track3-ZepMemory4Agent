#!/bin/sh
set -eu

docker compose run --rm app python -m src.demo_short_term
docker compose run --rm app python -m src.demo_sessions
docker compose run --rm app python -m src.local_baseline
docker compose run --rm app python -m src.episodic_maintenance
docker compose run --rm app python -m src.heartbeat --dry-run
