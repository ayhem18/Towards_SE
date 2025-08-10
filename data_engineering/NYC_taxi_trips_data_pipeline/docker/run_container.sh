# remove the container if it exists already
# docker ps -a | grep ny_c1 | awk '{print $1}' | xargs docker rm -f


docker rm -f ny_c1

# run the container
docker run --name ny_c1 -it \
    -e POSTGRES_USER=myuser \
    -e POSTGRES_PASSWORD=mypassword \
    -e POSTGRES_DB=ny_taxi_db \
    ny_taxi:1.0 