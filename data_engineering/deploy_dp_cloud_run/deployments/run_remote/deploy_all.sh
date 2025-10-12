#!/bin/bash
set -e

_SCHEDULE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_SCHEDULE_SCRIPT_DIR}/../utils/common.sh"
source "${_SCHEDULE_SCRIPT_DIR}/../utils/gcloud_utils.sh"

# --- SCRIPT ARGUMENTS ---
PIPELINE_NAME=$1
# SCHEDULE=$2 # e.g., "0 2 * * *" for 2 AM daily
SCHEDULE="*/15 * * * *" # every 10 minutes for now

if [[ -z "${PIPELINE_NAME}" ]]; then
    echo "Usage: $0 <pipeline-name> '<schedule-in-cron-format>'"
    exit 1
fi

# call the deploy_pipeline_gcloud.sh script
source "${_SCHEDULE_SCRIPT_DIR}/deploy_pipeline_google_run.sh" "${PIPELINE_NAME}"

SCHEDULER_JOB_NAME="${PIPELINE_NAME}-scheduler"


# the JOB_NAME is exported from the deploy_pipeline_gcloud.sh script 

# get the GCP_SCHEDULER_SERVICE_ACCOUNT_EMAIL from the gcloud_utils.sh script 
GCP_SCHEDULER_SERVICE_ACCOUNT_EMAIL=$(get_gcp_service_agent_email "cloudscheduler")

if [[ -z "${GCP_SCHEDULER_SERVICE_ACCOUNT_EMAIL}" ]]; then
    echo "Error: GCP_SCHEDULER_SERVICE_ACCOUNT_EMAIL is not set"
    exit 1
fi

# 

# echo "--> Creating Cloud Scheduler job: ${SCHEDULER_JOB_NAME} with schedule: ${SCHEDULE}"

# gcloud scheduler jobs create http "${SCHEDULER_JOB_NAME}" \
#     --project="${GCP_PROJECT_ID}" \
#     --location="${GCP_REGION}" \
#     --schedule="${SCHEDULE}" \
#     --uri="https://${GCP_REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${GCP_PROJECT_ID}/jobs/${JOB_NAME}:run" \
#     --http-method="POST" \
#     # --oauth-service-account-email="${GCP_SCHEDULER_SERVICE_ACCOUNT_EMAIL}" # This needs to be the Cloud Scheduler service agent



# echo "--- Granting Scheduler permission to invoke Cloud Run Job ---"
# gcloud run jobs add-iam-policy-binding "${JOB_NAME}" \
#     --project="${GCP_PROJECT_ID}" \
#     --region="${GCP_REGION}" \
#     --member="serviceAccount:${GCP_SCHEDULER_SERVICE_ACCOUNT_EMAIL}" \
#     --role="roles/run.invoker"

# echo "--- Scheduling complete for ${JOB_NAME} ---"
