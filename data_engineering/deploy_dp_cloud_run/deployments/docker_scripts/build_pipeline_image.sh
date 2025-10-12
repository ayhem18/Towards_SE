#!/bin/bash
set -e

# This script builds a specific pipeline's Docker image and pushes it to the Artifact Registry.
# Usage: ./deploy_pipeline.sh <pipeline-name> [--build_local]
# Example: ./deploy_pipeline.sh pipeline1 --build_local

_DEPLOY_PIPELINE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_DEPLOY_PIPELINE_SCRIPT_DIR}/../utils/common.sh"
# source "${_DEPLOY_PIPELINE_SCRIPT_DIR}/../utils/gcloud_utils.sh"

# --- 1. Parse Arguments ---
PIPELINE_NAME=""
BUILD_LOCAL=false
for arg in "$@"; do
    case $arg in
        --build-local)
        BUILD_LOCAL=true
        shift # Remove --build_local from processing
        ;;
        *)
        # It's not a flag, so it must be the pipeline name
        if [[ -z "${PIPELINE_NAME}" ]]; then
            PIPELINE_NAME=$arg
        fi
        shift # Remove generic argument from processing
        ;;
    esac
done

if [[ -z "${PIPELINE_NAME}" ]]; then
    echo "Error: No pipeline name provided."
    echo "Usage: $0 <pipeline-name> [--build_local]"
    exit 1
fi

# --- 2. Define Paths and Variables ---
_PROJECT_ROOT="${_DEPLOY_PIPELINE_SCRIPT_DIR}/../.."
PIPELINE_DIR="${_PROJECT_ROOT}/pipelines/${PIPELINE_NAME}"

if [[ ! -d "${PIPELINE_DIR}" ]]; then
    echo "Error: Pipeline directory not found at '${PIPELINE_DIR}'"
    exit 1
fi

# --- 3. Construct Image Tags ---
BASE_IMAGE_TAG="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REPO_NAME}/basi_dp:latest"
PIPELINE_IMAGE_TAG="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REPO_NAME}/${PIPELINE_NAME}:latest"

echo "--- Building and pushing image for pipeline: ${PIPELINE_NAME} ---"
echo "Pipeline Directory: ${PIPELINE_DIR}"
echo "Base Image: ${BASE_IMAGE_TAG}"
echo "Target Image: ${PIPELINE_IMAGE_TAG}"

# # --- 4. Build the Docker image for the registry ---
BUILD_ARGS="--build-arg BASE_IMAGE_TAG=${BASE_IMAGE_TAG}"

echo "The build arguments: ${BUILD_ARGS}"

echo "Building Docker image for registry..."
docker build ${BUILD_ARGS} -t "${PIPELINE_IMAGE_TAG}" "${PIPELINE_DIR}"

# --- 5. Push the image to Artifact Registry ---
echo "Pushing image to Artifact Registry..."
docker push "${PIPELINE_IMAGE_TAG}"


echo "--- Successfully built and pushed image: ${PIPELINE_IMAGE_TAG} ---"

# # --- 6. Build locally if the flag is set ---
if [[ "${BUILD_LOCAL}" = true ]]; then
    build_image_locally "${PIPELINE_NAME}" "${PIPELINE_DIR}" "${BUILD_ARGS}"
fi

echo "--- Successfully built image locally: ${PIPELINE_IMAGE_TAG} ---"

