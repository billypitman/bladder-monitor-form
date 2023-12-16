# Bladder Health Monitor

This repository contains a web form designed for monitoring bladder health in individuals with Spinal Cord Injury (SCI). It allows users to record their liquid intake and output. The form is built using Flask and packaged into a Docker image for easy deployment. After logging, the structured tabular data can then be connected to downstream analytics for visualization and analysis.

## Setup Instructions

### Database Connection
- **Azure SQL Database**: Before using the application, a valid Azure SQL database will need to be created, with its access credentials available.
- **Configuration**: Create a `.env` file in the project root directory with your database connection details, and azure container registry connection details if deploying to the azure container registry. Refer to the `.env.example` file for the format.

## Deployment Guide

### Local Deployment
- **Docker Image**: Run the `scripts/build_and_run.sh` bash script from the project root to build and run the Docker image locally.

### Deployment to Azure
- **Azure Container Registry**: To deploy the Docker image to Azure, execute the `scripts/deploy_to_azure.sh` bash script from the project root. 




