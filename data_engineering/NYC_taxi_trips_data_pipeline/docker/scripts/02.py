import os
import argparse
import pandas as pd

from pathlib import Path

def convert_parquet_to_csv(input_file: str) -> None:
    """Converts a Parquet file to a CSV file."""
    if not os.path.exists(input_file):
        raise ValueError(f"Input file not found at {input_file}")

    d = Path(input_file).parent
    file_name, ext = os.path.splitext(input_file)
    output_file = os.path.join(d, f'{file_name}.csv')

    df = pd.read_parquet(input_file)    
    df.to_csv(output_file, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a Parquet file to a CSV file.')
    parser.add_argument('--input_file', required=True, help='The path to the input .parquet file.')    
    args = parser.parse_args()    
    convert_parquet_to_csv(args.input_file)