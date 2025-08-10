-- the main point of this script is to load the data into the database

-- no need to create a database or call the 'use' command, since the docker image does this automatically if 


CREATE TABLE IF NOT EXISTS yellow_tripdata_2010_01 (
    "VendorID" TEXT,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count BIGINT,
    trip_distance DOUBLE PRECISION,
    "RatecodeID" DOUBLE PRECISION,
    store_and_fwd_flag TEXT,
    "PULocationID" BIGINT,
    "DOLocationID" BIGINT,
    payment_type BIGINT,
    fare_amount DOUBLE PRECISION,
    extra DOUBLE PRECISION,
    mta_tax DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    tolls_amount DOUBLE PRECISION,
    improvement_surcharge DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    congestion_surcharge DOUBLE PRECISION,
    airport_fee DOUBLE PRECISION
);


-- load the data from the parquet file 
COPY yellow_tripdata_2010_01 FROM '/usr/local/app/data/yellow_tripdata_2010-01.csv' 
WITH (FORMAT CSV, HEADER);

