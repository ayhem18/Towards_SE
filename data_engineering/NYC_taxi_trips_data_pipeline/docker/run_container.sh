# make sure the the docker image ny_taxi:1.0 exists
# TODO: make the script more flexible when it comes to image tag: (since the run command below is creating )
# one possible solution is to enforce passing a tag as an argument to the script


if ! docker images | grep ny_taxi; then
    # this builds an image with the tag as "latest"
    docker build -t ny_taxi .
fi

# if ny_c1 exists, then call the start command instead of the run command
if docker ps -a | grep ny_c1; then
    # check if the container is running : docker ps (without -a flag) returns only running containers
    
    if docker ps | grep ny_c1; then
        printf "Stopping existing container ny_c1\n"
        docker container stop ny_c1
    fi
    # start the container (again)
    docker container start ny_c1

else
    printf "Running new container ny_c1\n"
    # run the container
    # -d: run the container in detached mode
    # -e: set environment variables
    # --name: name the container
    # -p: exposes the port 5432 of the container to the host machine
    # not sure exactly how the  -p arguments work
    docker run --name ny_c1 \
        -e POSTGRES_USER=myuser \
        -e POSTGRES_PASSWORD=mypassword \
        -e POSTGRES_DB=ny_taxi_db \
        -p 5123:5432 \
        ny_taxi:latest

    # the run command might not work as expected
    # to verify this, call the docker ps -a followed by the grep command to capture whether the container is running or existed
    # if the container is exited, then remove the container and remove the image

    if docker ps -a | grep "Exited"; then
        # remove the container
        docker container rm ny_c1
        # remove the image
        docker image rm ny_taxi
    fi

fi


