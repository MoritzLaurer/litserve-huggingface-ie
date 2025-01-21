#!/bin/bash

# Configuration
DOCKER_USERNAME="moritzlaurer"
REPOSITORY_NAME="litserve-huggingface-ie-siglip"
VERSION="0.0.7-siglip-so400m-patch14-384"  # Change this when you want to update the version

# Build the Docker image
echo "Building Docker image..."
docker buildx create --use
docker buildx build --platform linux/amd64 \
    -t $DOCKER_USERNAME/$REPOSITORY_NAME:latest \
    -t $DOCKER_USERNAME/$REPOSITORY_NAME:$VERSION \
    --push .

# Verify the push
echo "Verifying push to Docker Hub..."
docker manifest inspect $DOCKER_USERNAME/$REPOSITORY_NAME:latest
docker manifest inspect $DOCKER_USERNAME/$REPOSITORY_NAME:$VERSION

echo "Done! Images pushed successfully as:"
echo "- $DOCKER_USERNAME/$REPOSITORY_NAME:latest"
echo "- $DOCKER_USERNAME/$REPOSITORY_NAME:$VERSION" 