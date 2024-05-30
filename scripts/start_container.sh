#!/bin/bash
set -e

# Pull the Docker image from Docker Hub
docker pull ajayadikari/chat-app-backend

# Run the Docker image as a container
docker run -d -p 8000:8000 ajayadikari/chat-app-backend