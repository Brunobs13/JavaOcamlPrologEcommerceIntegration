#!/usr/bin/env bash
set -euo pipefail

if [[ -f .env ]]; then
  while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    line="${raw_line#"${raw_line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"

    if [[ -z "$line" || "${line:0:1}" == "#" ]]; then
      continue
    fi

    if [[ "$line" != *"="* ]]; then
      continue
    fi

    key="${line%%=*}"
    value="${line#*=}"
    key="${key//[[:space:]]/}"
    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"

    if [[ "$value" =~ ^\".*\"$ ]]; then
      value="${value:1:${#value}-2}"
    elif [[ "$value" =~ ^\'.*\'$ ]]; then
      value="${value:1:${#value}-2}"
    fi

    if [[ -n "$key" ]]; then
      export "$key=$value"
    fi
  done < .env
fi

HOST="${APP_HOST:-0.0.0.0}"
PORT="${APP_PORT:-8080}"

PYTHONPATH=src uvicorn polyglot_commerce.api.app:app --host "$HOST" --port "$PORT"
