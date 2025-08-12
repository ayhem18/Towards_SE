CREATE TABLE IF NOT EXISTS yellow_tripdata_2010_01 (
    vendor_id              TEXT, 
    pickup_datetime        TIMESTAMP,
    dropoff_datetime       TIMESTAMP,
    passenger_count         INTEGER,
    trip_distance         TEXT,
    pickup_longitude      TEXT,
    pickup_latitude       TEXT,
    rate_code               INTEGER,
    store_and_fwd_flag    TEXT,
    dropoff_longitude     TEXT,
    dropoff_latitude      TEXT,
    payment_type           TEXT,
    fare_amount           TEXT,
    surcharge             TEXT,
    mta_tax               TEXT,
    tip_amount            TEXT,
    tolls_amount          TEXT,
    total_amount          TEXT
);


-- load the data from the parquet file 
COPY yellow_tripdata_2010_01 FROM '/usr/local/app/data/yellow_tripdata_2010-01.csv' 
WITH (FORMAT CSV, HEADER);

