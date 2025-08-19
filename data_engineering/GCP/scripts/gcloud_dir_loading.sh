#! /bin/bash
# this is a simple script to load load the contents of a directory into a GCP bucket 


# the script is written as follows: 

# 1. accepts 3 arguments: bucket name, folder name, path to a directory

# 2. checks if the bucket name exists

# 2. 1. if yes, check if the hierarichal structure is enabled

# 2. 2. if no create it

# 3. check if the folder exists

# 3. 1. if no create it

# 4. copy all the data from the local directory to the specified bucket’s folder 

