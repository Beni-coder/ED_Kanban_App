#!/usr/bin/env bash
set -e
docker compose up --build -d
echo ""
echo "Serveur demarre sur http://localhost:8000"
