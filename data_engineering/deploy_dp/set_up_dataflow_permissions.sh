#!/bin/bash
set -e

# This script should be in the same directory as your deployment script
# to source the common environment variables and utilities.
_PERMISSONS_SETUP_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_PERMISSONS_SETUP_SCRIPT_DIR}/common.sh"
source "${_PERMISSONS_SETUP_SCRIPT_DIR}/gcloud_utils.sh"

# 1. Define a name for your new worker service account
DP_WORKER_SA_NAME="dp-flex-worker-sa"

# 2. get the main bucket name from the arguments

_DP_MAIN_BUCKET_NAME="--main-bucket-name"

if [[ -z "${_DP_MAIN_BUCKET_NAME}" ]]; then
    echo "Error: Main bucket name is not set."
    exit 1
fi

echo "--- Setting up Dataflow Worker Service Account: ${DP_WORKER_SA_NAME} ---"

# 3. Create the user-managed service account
create_service_account_in_gcp "${DP_WORKER_SA_NAME}" "Dataflow Flex Template Worker"


# 4. Grant the service account the roles to access the artifact registry
grant_sa_permission_on_artifact_registry "${DP_WORKER_SA_NAME}" "roles/artifactregistry.repoAdmin"


# 4. Grant necessary project-level roles to the worker service account
# roles/dataflow.worker: Required for the service account to run as a Dataflow worker.
grant_sa_permission_on_project "${DP_WORKER_SA_NAME}" "roles/dataflow.worker"

# roles/dataflow.admin: Grants permissions to create and examine jobs.
grant_sa_permission_on_project "${DP_WORKER_SA_NAME}" "roles/dataflow.admin"

# 5. Grant storage permissions for staging, temp, and specification files
# roles/storage.objectAdmin: Allows the worker to read and write objects in your GCS bucket.
grant_sa_permission_on_bucket "${DP_MAIN_BUCKET_NAME}" "${DP_WORKER_SA_NAME}" "roles/storage.objectAdmin"



echo "--- Permissions setup complete for ${DP_WORKER_SA_NAME} ---"

# You can now export the service account email to use in your deployment script
export DP_WORKER_SA_EMAIL=$(get_service_account_email "${DP_WORKER_SA_NAME}")
echo "Service Account Email: ${DP_WORKER_SA_EMAIL}"