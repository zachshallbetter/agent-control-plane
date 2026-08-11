#!/usr/bin/env bash
set -euo pipefail
: "${EVENT_FILE:?EVENT_FILE is required}"
: "${PACKET_FILE:?PACKET_FILE is required}"
printf '%s\n' '{"event":"received","action":"classify"}'
PACKET="$PACKET_FILE" ./scripts/admission.sh
