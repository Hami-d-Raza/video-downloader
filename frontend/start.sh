#!/bin/bash
# Railway start script for frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    npm install
fi

# Build the frontend
npm run build

# Start preview server
npm run preview -- --host 0.0.0.0 --port ${PORT:-4173}
