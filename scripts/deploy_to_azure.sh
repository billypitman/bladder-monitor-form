#!/bin/bash
sh ./scripts/build_and_run.sh

docker login danhub.azurecr.io  
docker tag danhub-web danhub.azurecr.io/danhub_app:v1.2  
docker push danhub.azurecr.io/danhub_app:v1.2 