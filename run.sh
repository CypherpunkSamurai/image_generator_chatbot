#!/bin/sh
# Author: CypherpunkSamurai

# if .venv exists use python from .venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000