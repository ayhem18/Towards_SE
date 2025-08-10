import os
import argparse
import pandas as pd
import pyarrow.parquet as pq

from tqdm import tqdm
from pathlib import Path

def convert_parquet_to_csv(input_file: str, batch_size: int = 10000) -> None:
    """Converts a Parquet file to a CSV file in batches to manage memory usage."""
    if not os.path.exists(input_file):
        raise ValueError(f"Input file not found at {input_file}")

    output_file = Path(input_file).with_suffix('.csv')
    print(f"Converting {input_file} to {output_file} with batch size {batch_size}...")

    parquet_file = pq.ParquetFile(input_file)
    
    is_first_batch = True
    for batch in tqdm(parquet_file.iter_batches(batch_size=batch_size), total=parquet_file.num_row_groups, desc="Converting Parquet to CSV"):
        df = batch.to_pandas()
        
        if is_first_batch:
            # For the first batch, write with header and overwrite any existing file
            df.to_csv(output_file, index=False, mode='w', header=True)
            is_first_batch = False
        else:
            # For subsequent batches, append without header
            df.to_csv(output_file, index=False, mode='a', header=False)

        break # TODO: remove this (added to run at least the whole thing once and verify schema and data loading)
    # remove the parquet file
    print("Conversion complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a Parquet file to a CSV file.')
    parser.add_argument('--input_file', required=True, help='The path to the input .parquet file.')
    parser.add_argument('--batch_size', type=int, default=50000, help='The number of rows per batch for conversion.')
    args = parser.parse_args()    
    convert_parquet_to_csv(args.input_file, args.batch_size)