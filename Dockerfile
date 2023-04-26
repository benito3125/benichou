# The image used according to the technology/language
#FROM python:3.10-alpine
FROM docker-airbus-virtual.artifactory.2b82.aws.cloud.airbus.corp/jenkins/slaves/python:3.9

# Who will maintain this file
LABEL maintainer='guillain@airbus.com'

# Definne the worksspace folder
WORKDIR /app

# Copy local files into the container
COPY src /app
COPY requirements.txt /tmp/

# Install Python dependencies
RUN pip install -r /tmp/requirements.txt

# Run the following command when the container is starting
ENTRYPOINT python server.py --ip 0.0.0.0

