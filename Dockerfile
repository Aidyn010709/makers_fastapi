FROM python:3.10-slim AS deps
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY requirements.setup.txt /app/requirements.setup.txt
RUN apt-get update -y && apt-get -y install gcc
RUN pip --no-cache-dir install -r requirements.txt 
