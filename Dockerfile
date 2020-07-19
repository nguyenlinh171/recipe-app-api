# Image name
FROM python:3.7-alpine

# MAINTAINER instruction is deprecated and replaced with LABEL, i.e., the maintainer of the image
LABEL key="Lampire Ltd" 

# Set python unbuffered environment variable to 1 - run python in unbuffered mode - recommended for python run in docker container because it doesn't allow python to buffer the outputs, it'll print them out directly to avoid complication with the DOcker image - Data Buffer is a general computer science concept
ENV PYTHONUNBUFFERED=1.0

# Store dependencies in the requirements.txt in the docker image and Install the listed Dependencies using PIP. Copy the requirements file in the root folder to the requirments file in the docker image
COPY ./requirements.txt ./requirements.txt
RUN pip install -r /requirements.txt

# Make a directory (create an empty folder call app on the docking image, set it as the default directory, copy the app folder (inc. codes) in our local machine to the docker image) within the docker image to store the application source code
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create an user named "user" (can choose a different name to "user"), -D means creating an user which is used to run application only, and switch the user on docker to the new user created that is going to run the application using docker and
RUN adduser -D user
USER user
# The reason to create a new user is for security purposes, otherwise the image will run the application using the root account which is not recommended, creating the user to run the application only will limit the scope if a hacker get do within the image 
