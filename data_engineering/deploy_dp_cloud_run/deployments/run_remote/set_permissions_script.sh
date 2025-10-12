#!/bin/bash
set -e

# This script sets up a dedicated Service Account for a single pipeline.
_PERMISSONS_SETUP_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_PERMISSONS_SETUP_SCRIPT_DIR}/../utils/common.sh"
source "${_PERMISSONS_SETUP_SCRIPT_DIR}/../utils/gcloud_utils.sh" 

# --- SCRIPT ARGUMENTS ---
PIPELINE_SA_NAME=$1 # e.g., "my-pipeline-1-sa"
DP_MAIN_BUCKET_NAME=$2 # e.g., "ayhem-exp-bucket"

if [[ -z "${PIPELINE_SA_NAME}" || -z "${DP_MAIN_BUCKET_NAME}" ]]; then
    echo "Usage: $0 <service-account-name> <gcs-bucket-name>"
    exit 1
fi

echo "--- Setting up Service Account: ${PIPELINE_SA_NAME} ---"

# 1. Create the user-managed service account
create_service_account_in_gcp "${PIPELINE_SA_NAME}" "Service Account for ${PIPELINE_SA_NAME}"

# 2. Grant permissions needed by the DATAFLOW WORKERS
# These are the permissions the job needs while it's running.
echo "--> Granting permissions for Dataflow workers..."
grant_sa_permission_on_project "${PIPELINE_SA_NAME}" "roles/dataflow.worker"
grant_sa_permission_on_bucket "${DP_MAIN_BUCKET_NAME}" "${PIPELINE_SA_NAME}" "roles/storage.objectAdmin"

# 3. Grant permissions needed by the CLOUD RUN LAUNCHER
# The Cloud Run job needs these to submit the pipeline and act on behalf of the worker SA.
echo "--> Granting permissions for the Cloud Run launcher..."
grant_sa_permission_on_project "${PIPELINE_SA_NAME}" "roles/dataflow.admin"
# This critical permission allows the Cloud Run job to assign this SA to the Dataflow workers.
grant_sa_permission_on_self "${PIPELINE_SA_NAME}" "roles/iam.serviceAccountUser"

# 4. (Optional but Recommended) Grant Artifact Registry read access
# This allows the service account to be used for pulling its own image if needed,
# though Cloud Run usually handles this with its own service agent.
# grant_sa_permission_on_artifact_registry "${ARTIFACT_REPO_NAME}" "${PIPELINE_SA_NAME}" "roles/artifactregistry.reader"

echo "--- Permissions setup complete for ${PIPELINE_SA_NAME} ---"
export PIPELINE_SA_EMAIL=$(get_service_account_email "${PIPELINE_SA_NAME}")
echo "Service Account Email: ${PIPELINE_SA_EMAIL}"