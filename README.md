# bladder-health-monitor
This repository holds a web form to input liquid intake
and output as a means of monitoring bladder health in individuals
with SCI. This web form is built with Flask and deployed into a docker image. 

## Set up

To set up this repository, a connection with an Azure SQL database needs to be prepared.
This can be performed by configuring a .env file with the database connection information. See the .env.example file for a template. 

## Deployment

### Local deployment
To deploy the docker image locally, run the build_and_run.sh bash script.

### Deployment to azure
To deploy the docker image to azure container registry. Run the deploy_to_azure.sh bash script.




