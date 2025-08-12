-- Recreate target and staging to allow re-runs
DROP TABLE IF EXISTS yellow_tripdata_2010_01_stage;
DROP TABLE IF EXISTS yellow_tripdata_2010_01;

-- Target table with surrogate key

-- the copy method does not have a skip feature...
-- in other words, if a single row is invalid, the entire load will fail

-- so the solution is 2 folds:
-- 1. load the data into a staging table (one where the schema is all text without any constraints)
-- 2. create the correct schema and then insert, from the staging table, only the valid rows

CREATE TABLE IF NOT EXISTS yellow_tripdata_2010_01 (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vendor_id              TEXT, 
    pickup_datetime        TIMESTAMP,
    dropoff_datetime       TIMESTAMP,

    passenger_count        INTEGER CHECK (passenger_count IS NULL OR passenger_count >= 1),
    trip_distance          DOUBLE PRECISION CHECK (trip_distance IS NULL OR trip_distance >= 0),

    pickup_longitude       DOUBLE PRECISION CHECK (pickup_longitude IS NULL OR pickup_longitude BETWEEN -180 AND 180),
    pickup_latitude        DOUBLE PRECISION CHECK (pickup_latitude  IS NULL OR pickup_latitude  BETWEEN  -90 AND  90),
    rate_code              INTEGER,

    store_and_fwd_flag     TEXT,
    dropoff_longitude      DOUBLE PRECISION CHECK (dropoff_longitude IS NULL OR dropoff_longitude BETWEEN -180 AND 180),
    dropoff_latitude       DOUBLE PRECISION CHECK (dropoff_latitude  IS NULL OR dropoff_latitude  BETWEEN  -90 AND  90),

    payment_type           TEXT,

    fare_amount            DOUBLE PRECISION CHECK (fare_amount   IS NULL OR fare_amount   >= 0),
    surcharge              DOUBLE PRECISION CHECK (surcharge     IS NULL OR surcharge     >= 0),
    -- mta_tax can be negative
    mta_tax                DOUBLE PRECISION,
    tip_amount             DOUBLE PRECISION CHECK (tip_amount    IS NULL OR tip_amount    >= 0),
    tolls_amount           DOUBLE PRECISION CHECK (tolls_amount  IS NULL OR tolls_amount  >= 0),
    total_amount           DOUBLE PRECISION CHECK (total_amount  IS NULL OR total_amount  >= 0)
);

-- Optional: keep a natural-key uniqueness guard to prevent dup logical rows.
-- CREATE UNIQUE INDEX IF NOT EXISTS uq_yellow_vendor_pickup ON yellow_tripdata_2010_01 (vendor_id, pickup_datetime);

-- Staging table: all TEXT, no constraints
CREATE TABLE IF NOT EXISTS yellow_tripdata_2010_01_stage (
    vendor_id          TEXT,
    pickup_datetime    TEXT,
    dropoff_datetime   TEXT,
    passenger_count    TEXT,
    trip_distance      TEXT,
    pickup_longitude   TEXT,
    pickup_latitude    TEXT,
    rate_code          TEXT,
    store_and_fwd_flag TEXT,
    dropoff_longitude  TEXT,
    dropoff_latitude   TEXT,
    payment_type       TEXT,
    fare_amount        TEXT,
    surcharge          TEXT,
    mta_tax            TEXT,
    tip_amount         TEXT,
    tolls_amount       TEXT,
    total_amount       TEXT
);

-- Load raw CSV into staging
COPY yellow_tripdata_2010_01_stage
FROM '/usr/local/app/data/yellow_tripdata_2010-01.csv'
WITH (FORMAT CSV, HEADER);

-- Insert only valid rows into target; safe casts via regex to avoid aborting the load
INSERT INTO yellow_tripdata_2010_01 (
    vendor_id, pickup_datetime, dropoff_datetime, passenger_count,
    trip_distance, pickup_longitude, pickup_latitude, rate_code,
    store_and_fwd_flag, dropoff_longitude, dropoff_latitude, payment_type,
    fare_amount, surcharge, mta_tax, tip_amount, tolls_amount, total_amount
)
SELECT
    s.vendor_id,
    NULLIF(s.pickup_datetime,'')::timestamp,
    NULLIF(s.dropoff_datetime,'')::timestamp,
    CASE WHEN s.passenger_count ~ '^\d+$' THEN s.passenger_count::int ELSE NULL END,
    CASE WHEN s.trip_distance ~ '^-?\d+(\.\d+)?$' THEN s.trip_distance::double precision END,
    CASE WHEN s.pickup_longitude ~ '^-?\d+(\.\d+)?$' THEN s.pickup_longitude::double precision END,
    CASE WHEN s.pickup_latitude  ~ '^-?\d+(\.\d+)?$' THEN s.pickup_latitude::double precision  END,
    CASE WHEN s.rate_code ~ '^\d+$' THEN s.rate_code::int ELSE NULL END,
    s.store_and_fwd_flag,
    CASE WHEN s.dropoff_longitude ~ '^-?\d+(\.\d+)?$' THEN s.dropoff_longitude::double precision END,
    CASE WHEN s.dropoff_latitude  ~ '^-?\d+(\.\d+)?$' THEN s.dropoff_latitude::double precision  END,
    s.payment_type,
    CASE WHEN s.fare_amount   ~ '^-?\d+(\.\d+)?$' THEN s.fare_amount::double precision   END,
    CASE WHEN s.surcharge     ~ '^-?\d+(\.\d+)?$' THEN s.surcharge::double precision     END,
    CASE WHEN s.mta_tax       ~ '^-?\d+(\.\d+)?$' THEN s.mta_tax::double precision       END,
    CASE WHEN s.tip_amount    ~ '^-?\d+(\.\d+)?$' THEN s.tip_amount::double precision    END,
    CASE WHEN s.tolls_amount  ~ '^-?\d+(\.\d+)?$' THEN s.tolls_amount::double precision  END,
    CASE WHEN s.total_amount  ~ '^-?\d+(\.\d+)?$' THEN s.total_amount::double precision  END

FROM yellow_tripdata_2010_01_stage s

WHERE

    (s.passenger_count IS NULL OR (s.passenger_count ~ '^\d+$' AND s.passenger_count::int >= 1))
    AND (s.trip_distance     IS NULL OR (s.trip_distance     ~ '^-?\d+(\.\d+)?$' AND s.trip_distance::double precision     >= 0))
    AND (s.pickup_longitude  IS NULL OR (s.pickup_longitude  ~ '^-?\d+(\.\d+)?$' AND s.pickup_longitude::double precision  BETWEEN -180 AND 180))
    AND (s.pickup_latitude   IS NULL OR (s.pickup_latitude   ~ '^-?\d+(\.\d+)?$' AND s.pickup_latitude::double precision   BETWEEN  -90 AND  90))
    AND (s.dropoff_longitude IS NULL OR (s.dropoff_longitude ~ '^-?\d+(\.\d+)?$' AND s.dropoff_longitude::double precision BETWEEN -180 AND 180))
    AND (s.dropoff_latitude  IS NULL OR (s.dropoff_latitude  ~ '^-?\d+(\.\d+)?$' AND s.dropoff_latitude::double precision  BETWEEN  -90 AND  90))
    AND (s.fare_amount       IS NULL OR (s.fare_amount       ~ '^-?\d+(\.\d+)?$' AND s.fare_amount::double precision       >= 0))
    AND (s.surcharge         IS NULL OR (s.surcharge         ~ '^-?\d+(\.\d+)?$' AND s.surcharge::double precision         >= 0))
   
    AND (s.mta_tax           IS NULL OR  s.mta_tax           ~ '^-?\d+(\.\d+)?$')
    AND (s.tip_amount        IS NULL OR (s.tip_amount        ~ '^-?\d+(\.\d+)?$' AND s.tip_amount::double precision        >= 0))
    AND (s.tolls_amount      IS NULL OR (s.tolls_amount      ~ '^-?\d+(\.\d+)?$' AND s.tolls_amount::double precision      >= 0))
    AND (s.total_amount      IS NULL OR (s.total_amount      ~ '^-?\d+(\.\d+)?$' AND s.total_amount::double precision      >= 0));

-- Optional cleanup:
-- TRUNCATE yellow_tripdata_2010_01_stage;