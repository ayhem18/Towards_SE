# source the common script to have access to the common environment variables

set -e

_DP_DEPLOY_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "DP_DEPLOY_SCRIPT_DIR: ${_DP_DEPLOY_SCRIPT_DIR}"

source "${_DP_DEPLOY_SCRIPT_DIR}/common.sh"
source "${_GS_CLOUD_UTILS_DIR}/gcloud_utils.sh"

# according to this Google Cloud documentation: 
# https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates#create_bucket

# create a docker repository to save docker images
create_docker_repository 

# # configure the docker client to use the docker repository
# configure_docker_auth


# let's define the temporary and staging locations
DP_MAIN_BUCKET_NAME=ayhem-exp-bucket
DP_TEMP_FOLDER_LOCATION="gs://${DP_MAIN_BUCKET_NAME}/temp"
DP_STAGING_FOLDER_LOCATION="gs://${DP_MAIN_BUCKET_NAME}/staging"
DP_FLEX_SPECIFICATION_FOLDER_LOCATION="gs://${DP_MAIN_BUCKET_NAME}/flex-specs/flex_template_spec.json"

DP_BASIC_IMAGE_NAME="basic_dp_image"
IMAGE_PATH=${_DP_DEPLOY_SCRIPT_DIR}/dp


DP_SDK_CONTAINER_IMAGE="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REPO_NAME}/${DP_BASIC_IMAGE_NAME}:latest"

# TODO: understand what this command does exactly...
gcloud builds submit "${IMAGE_PATH}" --tag "${DP_SDK_CONTAINER_IMAGE}" --project "${GCP_PROJECT_ID}"







# build the dataflow flex template
gcloud dataflow flex-template build "${DP_FLEX_SPECIFICATION_FOLDER_LOCATION}"  \
    --image "${DP_SDK_CONTAINER_IMAGE}" \
    --sdk-language "PYTHON" \
    --project "${GCP_PROJECT_ID}"


DP_JOB_NAME="basic-dp-job-`date +%Y%m%d-%H%M%S`"

gcloud dataflow flex-template run "${DP_JOB_NAME}" \
    --template-file-gcs-location "${DP_FLEX_SPECIFICATION_FOLDER_LOCATION}" \
    --region "${GCP_REGION}" \
    --staging-location "${DP_STAGING_FOLDER_LOCATION}" \
    --project "${GCP_PROJECT_ID}" \
    # --parameters sdk_container_image=$DP_SDK_CONTAINER_IMAGE \ # not sure if this argument is needed
