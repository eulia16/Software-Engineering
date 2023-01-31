# Pull official base image for Python 3.10.8
FROM python:3.10.8-bullseye

# Create a new app directory (in the container) for the app files
RUN mkdir /flask-app

# Set the working directory
WORKDIR /flask-app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy host machine app files over to the container directory
COPY . /flask-app

# Run this bad boy
CMD python app.py