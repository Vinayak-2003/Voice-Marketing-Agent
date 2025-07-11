#!/bin/bash

# --- Basic Deployment Script for VoiceGenie ---
#
# This is a TEMPLATE script. In a real production environment, you would need
# to adapt this for your specific infrastructure (e.g., SSH keys, server IP,
# environment variable management like AWS Secrets Manager, etc.).
#
# Usage: ./scripts/deploy.sh

set -e # Exit immediately if a command exits with a non-zero status.

echo "🚀 Starting VoiceGenie deployment..."

# 1. Pull latest changes from the main branch
echo "    - Pulling latest code from git..."
git pull origin main

# 2. Rebuild and restart services with Docker Compose
#    --build: Forces a rebuild of the images (backend, frontend)
#    -d: Runs containers in detached mode
echo "    - Rebuilding and restarting Docker containers..."
docker-compose up -d --build

# 3. (Optional) Run database migrations
#    Our current setup uses `create_all`, which is simple. In production, you'd
#    use a migration tool like Alembic.
# echo "    - Running database migrations (if any)..."
# docker-compose exec backend alembic upgrade head

# 4. Clean up old, unused Docker images
echo "    - Pruning old Docker images..."
docker image prune -f

echo "✅ Deployment complete!"
echo "    API should be available at your server's address on port 8000."
echo "    Frontend should be available on port 80 (if configured)."