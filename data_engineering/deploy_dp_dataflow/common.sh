# a few environment variables are better defined for the entire project 
# to avoid some configuration / compatibility issues 

set -e


_COMMON_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GCP_PROJECT_ID=$(gcloud config get-value project)

GCP_REGION="us-central1"

ARTIFACT_REPO_NAME="test-docker-repo" 

DOCKER_CONFIG_FILE="${GCP_REGION}-docker.pkg.dev"


# Configure Docker to authenticate with Google Artifact Registry.
function configure_docker_auth() {
    echo "--- Authenticating Docker with gcloud for region '${GCP_REGION}' ---"
    gcloud auth configure-docker "${DOCKER_CONFIG_FILE}" --project="${GCP_PROJECT_ID}"
}

function create_docker_repository() {
    local artifact_repo_name=$1
    local artifact_repo_location=$2
    local artifact_repo_description=$3

    # set the default values if not provided
    if [[ -z "$artifact_repo_name" ]]; then
        artifact_repo_name=${ARTIFACT_REPO_NAME}
    fi
    
    if [[ -z "$artifact_repo_location" ]]; then
        artifact_repo_location=${GCP_REGION}
    fi

    if gcloud artifacts repositories describe "${ARTIFACT_REPO_NAME}" --location="${GCP_REGION}" --project="${GCP_PROJECT_ID}" >/dev/null 2>&1; then
        echo "Repository already exists."
        return 0
    fi

    echo "Repository not found. Creating it now..."
    # TODO check if I can pass an empty string for the description 
    # without getting an error or actually setting the description to an empty string

    if [[ -z "$artifact_repo_description" ]]; then
        gcloud artifacts repositories create ${artifact_repo_name} \
        --project=${GCP_PROJECT_ID} \
        --repository-format=docker \
        --location=${artifact_repo_location}
    else
        gcloud artifacts repositories create ${artifact_repo_name} \
        --project=${GCP_PROJECT_ID} \
        --repository-format=docker \
        --location=${artifact_repo_location} \
        --description=${artifact_repo_description}
    fi

}
