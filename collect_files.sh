#!/bin/bash


if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi


SCRIPT_DIR=$(dirname "$(realpath "$0")")
python3 "${SCRIPT_DIR}/collect_files.py" "$@"
