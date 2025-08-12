#!/bin/bash
set -e


printf "Activating virtual environment\n"
. /usr/local/app/image_env/bin/activate 

# convert parquet to csv
printf "Converting parquet to CSV\n"
PARQUET_FILE_PATH="/usr/local/app/data/yellow_tripdata_2010-01.parquet"
python3 /docker-entrypoint-initdb.d/convert_data.py --input_file $PARQUET_FILE_PATH

# Load data into PostgreSQL
printf "Loading data into PostgreSQL\n"
psql -v --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/load_data.sql