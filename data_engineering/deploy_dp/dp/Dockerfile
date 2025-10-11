# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local package to the container
COPY ./mypack /app/mypack
COPY main.py .

# Install the package
RUN pip install --no-cache-dir -e ./mypack

# For more informaiton, see: https://cloud.google.com/dataflow/docs/guides/templates/configuring-flex-templates
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/main.py"

# Optionally, verify that dependencies are not conflicting.
# A conflict may or may not be significant for your pipeline.
RUN pip check

# Optionally, list all installed dependencies.
# The output can be used to seed requirements.txt for reproducible builds.
RUN pip freeze

# Set the entrypoint to Apache Beam SDK launcher, which allows this image
# to be used as an SDK container image.
ENTRYPOINT ["/opt/apache/beam/boot"]