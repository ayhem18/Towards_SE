# the main point of this deplo

_DEPLOY_BASE_IMAGE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "${_DEPLOY_BASE_IMAGE_SCRIPT_DIR}/../utils/common.sh"
source "${_DEPLOY_BASE_IMAGE_SCRIPT_DIR}/../utils/gcloud_utils.sh"

create_docker_repository

configure_docker_auth

# the next step is to build and push to the artifact registry

_BASE_IMAGE_NAME="basi_dp"
_BASE_IMAGE_DIR="${_DEPLOY_BASE_IMAGE_SCRIPT_DIR}/../mypack_package"
_DOCKER_TAG="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REPO_NAME}/${_BASE_IMAGE_NAME}:latest"

# --- Parse command-line arguments ---
BUILD_LOCAL=false
if [[ "$1" == "--build_local" ]]; then
    BUILD_LOCAL=true
fi

echo "--- Building and tagging image for Artifact Registry ---"
docker build -t "${_DOCKER_TAG}" "${_BASE_IMAGE_DIR}"

# --- Build locally if the flag is set ---
if [[ "${BUILD_LOCAL}" = true ]]; then
    build_image_locally "${_BASE_IMAGE_NAME}" "${_BASE_IMAGE_DIR}"
fi

echo "--- Pushing image to Artifact Registry ---"
docker push "${_DOCKER_TAG}"

echo "Successfully pushed image: ${_DOCKER_TAG}"
