#!/bin/bash
# Railway start script for backend

# Install dependencies if needed
if [ ! -d "venv" ]; then
    python -m pip install --upgrade pip
    pip install -r requirements.txt
fi

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
