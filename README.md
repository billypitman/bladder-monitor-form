# danhub


## Commands for setting up docker images

### Local

docker-compose build  
docker-compose up  

### Deploying to Azure Container Registry
First create an image using the commands in Local, then use the following commands:  

docker login danhub.azurecr.io  
docker tag danhub-web danhub.azurecr.io/danhub_app:vX.Y  
docker push danhub.azurecr.io/danhub_app:vX.Y  



