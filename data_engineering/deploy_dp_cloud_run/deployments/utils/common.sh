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


# function run_local_build() {
#     local image_name=$1
#     local container_name=$2
#     local image_dir=$3
#     local build_target=$4

#     echo "--- Building Docker image locally ---"

#     # TODO: add image pruning !!

#     docker build --target "${build_target}" -t "${image_name}:local" "${image_dir}"
    
#     echo "--- Stopping and removing existing container instance ---"
#     if [[ $(docker ps -a --filter "name=${container_name}" --format '{{.Names}}') ]]; then
#         docker stop "${container_name}"
#         docker rm "${container_name}"
#     fi

#     echo "--- Running new container instance ---"
#     GCP_ADC_PATH="${HOME}/.config/gcloud/application_default_credentials.json"
#     if [ ! -f "$GCP_ADC_PATH" ]; then
#         echo "Error: Application Default Credentials not found. Please run 'gcloud auth application-default login'."
#         exit 1
#     fi

#     docker run -d --name "${container_name}" \
#         -p 8080:8080 \
#         -v "${GCP_ADC_PATH}:/app/credentials.json" \
#         -e "GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json" \
#         "${image_name}:local"

#     echo "Container '${container_name}' is running. View logs with 'docker logs -f ${container_name}'"
# }

# # Function to build and push the image to Google Artifact Registry
# function run_cloud_build() {
#     local docker_tag=$1
#     local image_dir=$2
#     local build_target=$3

#     ensure_artifact_registry_repo
#     configure_docker_auth

#     echo "--- Building and tagging image for Artifact Registry ---"
#     docker build --target "${build_target}" -t "${docker_tag}" "${image_dir}"

#     echo "--- Pushing image to Artifact Registry ---"
#     docker push "${docker_tag}"

#     echo "Successfully pushed image: ${docker_tag}"
# }

# Function to build a docker image with a ':local' tag.
function build_image_locally() {
    local image_name=$1
    local image_dir=$2
    local build_args=$3

    local local_tag="${image_name}:local"

    echo "--- Building Docker image locally with tag: ${local_tag} ---"

    local build_command="docker build  -t ${local_tag} ${build_args} ${image_dir}"
    echo "The command: ${build_command}"
    eval "${build_command}"

    echo "--- Successfully built local image: ${local_tag} ---"
}
