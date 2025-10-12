FROM python:3.11-slim

WORKDIR /app

COPY ./mypack /app/mypack

RUN pip install --no-cache-dir -e ./mypack

# the main point of this image is to save the common dependencies for all pipelines.
# deploy the image to the artifact registry.
# the pipelines images will be built on top of the image saved in the artifact registry.