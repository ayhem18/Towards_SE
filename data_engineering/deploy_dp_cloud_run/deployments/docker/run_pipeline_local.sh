set -e

pipeline_name=$1

command="""
docker run --rm \
  -it \
  -v /home/ayhem18/.config/gcloud/application_default_credentials.json:/app/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  "${pipeline_name}:local"
"""

echo "The command: ${command}"

eval "${command}"
  