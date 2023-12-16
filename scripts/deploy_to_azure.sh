#!/bin/bash
echo "Building docker container"
docker-compose build  

source .env

echo "Pushing to azure container registry"
docker login $CONTAINER_REGISTRY_LOGIN_SERVER  
docker tag $DOCKER_IMAGE_NAME $CONTAINER_REGISTRY_LOGIN_SERVER/$CONTAINER_REGISTRY_REPOSITORY:v$APP_VERSION 
docker push $CONTAINER_REGISTRY_LOGIN_SERVER/$CONTAINER_REGISTRY_REPOSITORY:v$APP_VERSION