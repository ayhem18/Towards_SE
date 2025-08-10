#!/bin/bash
set -e

# Convert parquet to CSV using the Python script
# for the python file to run, the virtual environment needs to be activated

printf "Activating virtual environment\n"

. /usr/local/app/image_env/bin/activate 

printf "Converting parquet to CSV\n"

python3 /docker-entrypoint-initdb.d/convert_data.py --input_file /usr/local/app/data/yellow_tripdata_2010-01.parquet

# The output file will be /usr/local/app/data/yellow_tripdata_2010-01.csv
CSV_FILE_PATH="/usr/local/app/data/yellow_tripdata_2010-01.csv"

printf "Loading data into PostgreSQL\n"

# Load data into PostgreSQL
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/load_data.sql