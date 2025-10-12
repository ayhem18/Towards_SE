# use a larger image to have have the apache beam sdk installed without further headache 
FROM python:3.11-slim

# Copy SDK entrypoint binary from Apache Beam image, which makes it possible to
# use the image as SDK container image. If you explicitly depend on
# apache-beam in setup.py, use the same version of Beam in both files.
COPY --from=apache/beam_python3.11_sdk:2.54.0 /opt/apache/beam /opt/apache/beam

# Copy Flex Template launcher binary from the launcher image, which makes it
# possible to use the image as a Flex Template base image.
COPY --from=gcr.io/dataflow-templates-base/python311-template-launcher-base:20230622_RC00 /opt/google/dataflow/python_template_launcher /opt/google/dataflow/python_template_launcher

# Set the working directory in the container
WORKDIR /app

# Copy the local package to the container
COPY ./mypack /app/mypack
COPY main.py .

# Install the package
RUN pip install --no-cache-dir -e ./mypack

# For more informaiton, see: https://cloud.google.com/dataflow/docs/guides/templates/configuring-flex-templates
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/app/main.py"

# Optionally, verify that dependencies are not conflicting.
# A conflict may or may not be significant for your pipeline.
RUN pip check

# Optionally, list all installed dependencies.
# The output can be used to seed requirements.txt for reproducible builds.
RUN pip freeze

# Set the entrypoint to Apache Beam SDK launcher, which allows this image
# to be used as an SDK container image.
ENTRYPOINT ["/opt/apache/beam/boot"]