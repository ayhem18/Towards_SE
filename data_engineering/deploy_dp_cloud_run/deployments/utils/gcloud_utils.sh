# !/bin/bash
set -e # exit immediately if a command exits with a non-zero status

_GS_CLOUD_UTILS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${_GS_CLOUD_UTILS_DIR}/common.sh"


function set_secret_in_gcp() {
    local secret_name=$1
    local secret_env_var_name=$2 # Renamed for clarity

    # Check if the environment variable (whose name is in secret_env_var_name) is set
    if [[ -z "${!secret_env_var_name}" ]]; then
        # This error message is now dynamic and more helpful!
        echo "Error: Environment variable '${secret_env_var_name}' is not set. It is required to create the secret."
        exit 1
    fi

    # Check if the secret already exists. If so, do nothing.
    if gcloud secrets describe "${secret_name}" --project="${GCP_PROJECT_ID}" >/dev/null 2>&1; then
        echo "--> Secret '${secret_name}' already exists. Skipping creation."
        return
    fi

    echo "--> Secret '${secret_name}' not found. Creating it now..."

    # Use indirect expansion to get the secret's VALUE and pipe it to gcloud
    echo -n "${!secret_env_var_name}" | gcloud secrets create "${secret_name}" \
        --project="${GCP_PROJECT_ID}" \
        --replication-policy="automatic" \
        --data-file=-
}


function get_service_account_email() {
    local service_account_name=$1
    local service_account_email="${service_account_name}@${GCP_PROJECT_ID}.iam.gserviceaccount.com"
    echo "${service_account_email}"
}


function create_service_account_in_gcp() {
    local service_account_name=$1
    local service_account_display_name=$2 

    local service_account_email=$(get_service_account_email "${service_account_name}")

	gcloud iam service-accounts describe "${service_account_email}" --project="${GCP_PROJECT_ID}" >/dev/null 2>&1 || {
		echo "Service account not found. Creating it now..."
		gcloud iam service-accounts create "${service_account_name}" \
		--project="${GCP_PROJECT_ID}" \
		--display-name="${service_account_display_name}"
	}


}

function grant_sa_permission_on_project() {
    local service_account_name=$1
    local role=$2
    local service_account_email
    service_account_email=$(get_service_account_email "${service_account_name}")

    echo "--> Granting Service Account '${service_account_name}' the project-level role '${role}'..."
    gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
        --member="serviceAccount:${service_account_email}" \
        --role="${role}" \
        --condition=None
}


function grant_sa_permission_on_self() {
    local service_account_name=$1
    local role=$2
    local service_account_email
    service_account_email=$(get_service_account_email "${service_account_name}")

    echo "--> Granting SA '${service_account_name}' the role '${role}' on ITSELF..."
    gcloud iam service-accounts add-iam-policy-binding "${service_account_email}" \
        --member="serviceAccount:${service_account_email}" \
        --role="${role}" \
        --project="${GCP_PROJECT_ID}"
}


function grant_service_account_resource_permission() {
    local resource_name=$1
    local role=$2
    local service_account_name=$3

    local service_account_email=$(get_service_account_email "${service_account_name}")

    echo "--> Granting service account permission to access the resource: ${resource_name} for the following role: ${role}"
    gcloud resource-manager add-iam-policy-binding "${resource_name}" \
        --project="${GCP_PROJECT_ID}" \
        --member="serviceAccount:${service_account_email}" \
        --role="${role}"
}


function grant_sa_permission_on_secret() {
    local secret_name=$1
    local service_account_name=$2
    local role="roles/secretmanager.secretAccessor" # Usually you only need this role
    local service_account_email
    service_account_email=$(get_service_account_email "${service_account_name}")

    echo "--> Granting SA '${service_account_name}' the role '${role}' on SECRET '${secret_name}'..."
    gcloud secrets add-iam-policy-binding "${secret_name}" \
        --project="${GCP_PROJECT_ID}" \
        --member="serviceAccount:${service_account_email}" \
        --role="${role}" \
        --condition=None
}


function grant_sa_permission_on_bucket() {
    local bucket_name=$1
    local service_account_name=$2
    local role=$3
    local service_account_email
    service_account_email=$(get_service_account_email "${service_account_name}")

    # if bucket name does not start with gs://, add it
    if [[ "${bucket_name}" != "gs://"* ]]; then
        bucket_name="gs://${bucket_name}"
    fi

    echo "--> Granting SA '${service_account_name}' the role '${role}' on BUCKET '${bucket_name}'..."
    gcloud storage buckets add-iam-policy-binding "${bucket_name}" \
        --member="serviceAccount:${service_account_email}" \
        --role="${role}" \
        --project="${GCP_PROJECT_ID}"
}


function ensure_pubsub_topic_exists() {
    local topic_name=$1

    echo "--> Ensuring Pub/Sub topic '${topic_name}' exists..."
    if gcloud pubsub topics describe "${topic_name}" --project="${GCP_PROJECT_ID}" >/dev/null 2>&1; then
        echo "Topic already exists."
    else
        echo "Topic not found. Creating it now..."
        gcloud pubsub topics create "${topic_name}" --project="${GCP_PROJECT_ID}"
    fi
}


function ensure_gcs_bucket_exists() {
    local bucket_name=$1
    echo "--> Ensuring GCS bucket '${bucket_name}' exists..."
    if ! gcloud storage buckets describe "gs://${bucket_name}" --project="${GCP_PROJECT_ID}" >/dev/null 2>&1; then
        echo "Bucket not found. Creating it now..."
        gcloud storage buckets create "gs://${bucket_name}" --project="${GCP_PROJECT_ID}" --location="${GCP_REGION}"
    else
        echo "Bucket already exists."
    fi
}


# Add these new functions to your gcloud_utils.sh script

# =====================================================================
# Function to get the full email address of a Google-managed Service Agent.
# Usage: get_gcp_service_agent_email "cloudscheduler"
# =====================================================================
function get_gcp_service_agent_email() {
    local service_name="$1"
    local project_number

    # First, get the unique project number for the current project ID.
    project_number=$(gcloud projects describe "${GCP_PROJECT_ID}" --format='value(projectNumber)')

    local service_agent_email=""
    case "${service_name}" in
        cloudscheduler)
            service_agent_email="service-${project_number}@gcp-sa-cloudscheduler.iam.gserviceaccount.com"
            ;;
        storage)
            service_agent_email="service-${project_number}@gs-project-accounts.iam.gserviceaccount.com"
            ;;
        "pubsub" | "Pub/Sub")
            service_agent_email="service-${project_number}@gcp-sa-pubsub.iam.gserviceaccount.com"
            ;;
        # Add other service agents here as needed in the future
        *)
            echo "Error: Unknown service agent name '${service_name}'." >&2
            return 1
            ;;
    esac
    echo "${service_agent_email}"
}


# =====================================================================
# Function to grant a role TO a Google Service Agent ON a specific resource,
# typically your own custom service account.
# Usage: grant_role_to_gcp_service_agent "cloudscheduler" "roles/iam.serviceAccountTokenCreator" "your-sa@..."
# =====================================================================
function grant_role_to_gcp_service_agent() {
    local service_agent_name="$1"
    local role_to_grant="$2"
    local on_behalf_of_sa_email="$3" # The email of YOUR custom SA

    local service_agent_email
    service_agent_email=$(get_gcp_service_agent_email "${service_agent_name}")

    if [[ -z "${service_agent_email}" ]]; then
        return 1 # Error message was already printed by the helper function
    fi

    echo "--> Granting GCP Service Agent '${service_agent_name}'"
    echo "    the role '${role_to_grant}'"
    echo "    on Service Account '${on_behalf_of_sa_email}'..."

    # This command modifies the IAM policy of YOUR service account.
    # It allows the --member (the GCP Service Agent) to perform an action.
    gcloud iam service-accounts add-iam-policy-binding "${on_behalf_of_sa_email}" \
        --project="${GCP_PROJECT_ID}" \
        --member="serviceAccount:${service_agent_email}" \
        --role="${role_to_grant}"
}


function grant_sa_permission_on_artifact_registry() {
    local artifact_registry_name=$1
    local service_account_name=$2
    local role=$3
    local service_account_email
    service_account_email=$(get_service_account_email "${service_account_name}")

    echo "--> Granting SA '${service_account_name}' the role '${role}' on ARTIFACT REGISTRY..."



    gcloud artifacts repositories add-iam-policy-binding "${artifact_registry_name}" \
    --location=${GCP_REGION} \
    --member="serviceAccount:${service_account_email}" \
    --role="${role}"
}


function deploy_cloud_run_job() {
    local job_name=$1
    local gcloud_job_args=$2

    echo "--> Checking if job '${job_name}' already exists..."
    # We check for existence by trying to describe the job.
    # The output is silenced (>/dev/null 2>&1) because we only care about the exit code.
    # If the exit code is 0 (success), the job exists.
    if gcloud run jobs describe "${job_name}" --project="${GCP_PROJECT_ID}" --region="${GCP_REGION}" >/dev/null 2>&1; then
    echo "--> Job exists. Applying updates..."
    gcloud run jobs update "${job_name}" \
        --project="${GCP_PROJECT_ID}" \
        --region="${GCP_REGION}" \
        "${gcloud_job_args[@]}"
    else
    echo "--> Job does not exist. Creating a new one..."
    gcloud run jobs create "${job_name}" \
        --project="${GCP_PROJECT_ID}" \
        --region="${GCP_REGION}" \
        "${gcloud_job_args[@]}"
    fi
}

