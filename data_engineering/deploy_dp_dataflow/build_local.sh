docker run --rm \
  -it \
  --entrypoint /bin/bash \
  -v /home/ayhem18/.config/gcloud/application_default_credentials.json:/app/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  dp