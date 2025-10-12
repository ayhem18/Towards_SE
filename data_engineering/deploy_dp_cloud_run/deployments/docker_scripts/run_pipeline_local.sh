#!/bin/bash
set -e

_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_SCRIPT_DIR}/../utils/common.sh"
source "${_SCRIPT_DIR}/../utils/gcloud_utils.sh"

PIPELINE_NAME=$1
if [[ -z "${PIPELINE_NAME}" ]]; then
    echo "Usage: $0 <pipeline-name>"
    exit 1
fi

# --- Define pipeline-specific variables ---
DP_MAIN_BUCKET_NAME="ayhem-exp-bucket" # As seen in other scripts
PIPELINE_SA_NAME="${PIPELINE_NAME}-sa"
PIPELINE_SA_EMAIL=$(get_service_account_email "${PIPELINE_SA_NAME}")
STAGING_LOCATION="gs://${DP_MAIN_BUCKET_NAME}/staging"
TEMP_LOCATION="gs://${DP_MAIN_BUCKET_NAME}/temp"

# --- Construct the full image tag from the Artifact Registry ---
# This is the image the Dataflow workers will pull.
PIPELINE_IMAGE_TAG="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REPO_NAME}/${PIPELINE_NAME}:latest"

# --- Check for local credentials ---
GCP_ADC_PATH="${HOME}/.config/gcloud/application_default_credentials.json"
if [ ! -f "$GCP_ADC_PATH" ]; then
    echo "Error: Application Default Credentials not found at '${GCP_ADC_PATH}'."
    echo "Please run 'gcloud auth application-default login'."
    exit 1
fi

echo "--- Running pipeline '${PIPELINE_NAME}' locally, targeting DataflowRunner ---"
echo "Project: ${GCP_PROJECT_ID}, Region: ${GCP_REGION}"
echo "Service Account: ${PIPELINE_SA_EMAIL}"

# The arguments after the image name are passed directly to the CMD in the Dockerfile
docker run --rm \
  -it \
  -v "${GCP_ADC_PATH}:/app/credentials.json" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  "${PIPELINE_NAME}:local" \
  --runner=DataflowRunner \
  --project="${GCP_PROJECT_ID}" \
  --region="${GCP_REGION}" \
  --staging_location="${STAGING_LOCATION}" \
  --temp_location="${TEMP_LOCATION}" \
  --service_account_email="${PIPELINE_SA_EMAIL}" \
  --sdk_container_image="${PIPELINE_IMAGE_TAG}"

echo "--- Pipeline execution command sent ---"
  