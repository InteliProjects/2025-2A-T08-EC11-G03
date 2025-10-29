#!/usr/bin/env bash
set -euo pipefail

log() {
  printf '[entrypoint] %s\n' "$*"
}

if command -v prisma >/dev/null 2>&1; then
  log "Generating Prisma client..."
  prisma generate
  if [[ -n "${DATABASE_URL:-}" ]]; then
    should_migrate="${RUN_PRISMA_MIGRATE:-true}"
    if [[ "${should_migrate,,}" != "false" ]]; then
      log "Running Prisma migrations..."
      prisma migrate deploy
    else
      log "Skipping Prisma migrations because RUN_PRISMA_MIGRATE=${should_migrate}"
    fi
  else
    log "Skipping Prisma migrations because DATABASE_URL is not set"
  fi
else
  log "Prisma CLI not found on PATH"
fi

exec "$@"
