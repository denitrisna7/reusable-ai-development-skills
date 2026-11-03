#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-.}"

python3 "${SCRIPT_DIR}/setup-project.py" "${TARGET_DIR}" "${@:2}"
