#!/bin/bash

# Configuration
DOCKER_USERNAME="moritzlaurer"
REPOSITORY_NAME="litserve-huggingface-ie-siglip"
OLD_VERSION="0.0.7"  # Specify the existing tag
NEW_VERSION="0.0.7-siglip-base-patch16-224"  # Specify your desired new tag

# Pull the existing image with platform specification
echo "Pulling existing image..."
docker pull --platform linux/amd64 $DOCKER_USERNAME/$REPOSITORY_NAME:$OLD_VERSION

# Retag the image
echo "Retagging image..."
docker tag $DOCKER_USERNAME/$REPOSITORY_NAME:$OLD_VERSION $DOCKER_USERNAME/$REPOSITORY_NAME:$NEW_VERSION

# Push the new tag
echo "Pushing new tag to Docker Hub..."
docker push $DOCKER_USERNAME/$REPOSITORY_NAME:$NEW_VERSION

echo "Done! Image retagged and pushed as:"
echo "- $DOCKER_USERNAME/$REPOSITORY_NAME:$NEW_VERSION" 