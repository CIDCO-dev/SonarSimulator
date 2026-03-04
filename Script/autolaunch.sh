#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERIAL_PORT="${SONAR_SERIAL_PORT:-/dev/ttyUSB0}"
BAUD_RATE="${SONAR_BAUD_RATE:-9600}"
SENTENCE_TYPE="${SONAR_SENTENCE_TYPE:-dpt}"

exec python3 "${SCRIPT_DIR}/sonar_simulator.py" \
  "${SERIAL_PORT}" \
  "${BAUD_RATE}" \
  --sentence-type "${SENTENCE_TYPE}"
