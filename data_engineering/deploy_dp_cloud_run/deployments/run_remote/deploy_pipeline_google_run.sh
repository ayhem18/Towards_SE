#!/bin/bash
set -e

_DEPLOY_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_DEPLOY_SCRIPT_DIR}/../utils/common.sh"
source "${_DEPLOY_SCRIPT_DIR}/../utils/gcloud_utils.sh" # Assumes _GS_CLOUD_UTILS_DIR is in common.sh

# --- SCRIPT ARGUMENTS ---
PIPELINE_NAME=$1         # e.g., "my-pipeline-1"
PIPELINE_SA_NAME="${PIPELINE_NAME}-sa"

PIPELINE_IMAGE_TAG="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REPO_NAME}/${PIPELINE_NAME}:latest"
DP_MAIN_BUCKET_NAME="ayhem-exp-bucket"

if [[ -z "${PIPELINE_NAME}" ]]; then
    echo "Usage: $0 <pipeline-name>"
    exit 1
fi

# if [[ -z "$1" || -z "$2" || -z "$3" || -z "$4" ]]; then
#     echo "Usage: $0 <pipeline-name> <image-tag> <service-account-name> <bucket-name>"
#     exit 1
# fi

PIPELINE_SA_EMAIL=$(get_service_account_email "${PIPELINE_SA_NAME}")
JOB_NAME="${PIPELINE_NAME}-job"
STAGING_LOCATION="gs://${DP_MAIN_BUCKET_NAME}/staging"
TEMP_LOCATION="gs://${DP_MAIN_BUCKET_NAME}/temp"

# INPUT_PATTERN="gs://${DP_MAIN_BUCKET_NAME}/data/data_*.json"
# OUTPUT_PATH="gs://${DP_MAIN_BUCKET_NAME}/output/${PIPELINE_NAME}/" # Note: path for output files

# call the set_permissions_script.sh script
source "${_DEPLOY_SCRIPT_DIR}/set_permissions_script.sh" "${PIPELINE_NAME}" "${DP_MAIN_BUCKET_NAME}"


echo "--- Creating/Updating Cloud Run Job: ${JOB_NAME} ---"


GCLOUD_JOB_ARGS=(
  "--image=${PIPELINE_IMAGE_TAG}"
  "--service-account=${PIPELINE_SA_EMAIL}"
  "--task-timeout=600" # 10 minutes; adjust as needed for job submission time
  "--args=--runner=DataflowRunner"
  "--args=--project=${GCP_PROJECT_ID}"
  "--args=--region=${GCP_REGION}"
  "--args=--staging_location=${STAGING_LOCATION}"
  "--args=--temp_location=${TEMP_LOCATION}"
  "--args=--service_account_email=${PIPELINE_SA_EMAIL}"
  "--args=--sdk_container_image=${PIPELINE_IMAGE_TAG}"
)

deploy_cloud_run_job "${JOB_NAME}" "${GCLOUD_JOB_ARGS}"

echo "--- Cloud Run Job setup complete. You can now run it manually or schedule it. ---"
