#!/bin/bash
echo "Building docker container"
docker-compose build  
echo "Creating image"
docker-compose up 