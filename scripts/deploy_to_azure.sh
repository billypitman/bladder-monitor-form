#!/bin/bash
echo "Building docker container"
docker-compose build  

APP_VERSION=$(python -c "from app.version import APP_VERSION; print(APP_VERSION)")

source .env

echo "Pushing to azure container registry"
docker login $CONTAINER_REGISTRY_LOGIN_SERVER  
docker tag $DOCKER_IMAGE_NAME $CONTAINER_REGISTRY_LOGIN_SERVER/$CONTAINER_REGISTRY_REPOSITORY:v$APP_VERSION 
docker push $CONTAINER_REGISTRY_LOGIN_SERVER/$CONTAINER_REGISTRY_REPOSITORY:v$APP_VERSION