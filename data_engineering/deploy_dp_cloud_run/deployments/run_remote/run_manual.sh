set -e

_RUN_MANUAL_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_RUN_MANUAL_SCRIPT_DIR}/../utils/common.sh"
# source "${_RUN_MANUAL_SCRIPT_DIR}/../utils/gcloud_utils.sh"

# --- SCRIPT ARGUMENTS ---

PIPELINE_NAME=$1

if [[ -z "${PIPELINE_NAME}" ]]; then
    echo "Usage: $0 <pipeline-name>"
    exit 1
fi

JOB_NAME="${PIPELINE_NAME}-job"

echo "--> Executing Cloud Run job: ${JOB_NAME}"

gcloud run jobs execute "${JOB_NAME}" \
  --region="${GCP_REGION}" \
  --project="${GCP_PROJECT_ID}" \
  --wait