# Docker image with Python3, poyodbc, MS ODBC 18 driver (SQL Server)

# Use official Python base image
FROM python:3.11-bullseye

# Set working directory
WORKDIR /app

# Send Python output streams to container log
ENV PYTHONUNBUFFERED 1

# Update apt-get
RUN apt-get update

# Install ggc
RUN apt-get install gcc

# Install FreeTDS and dependencies
RUN apt-get install unixodbc -y
RUN apt-get install unixodbc-dev -y
RUN apt-get install freetds-dev -y
RUN apt-get install freetds-bin -y
RUN apt-get install tdsodbc -y
RUN apt-get install --reinstall build-essential -y

# Populate "odbcinst.ini" file
RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

# ODBC driver dependencies
RUN apt-get install apt-transport-https 
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install ODBC driver
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18

# Configure ENV for /bin/bash to use MSODBCSQL18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bash_profile 
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc 

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY /app .

EXPOSE 5000

CMD python /app/app.py