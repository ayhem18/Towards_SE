import argparse
import os, csv

import pandas as pd
from tqdm import tqdm
from itertools import islice
from datasets import load_dataset

def load_dataset_way1(num_samples: int = 100000):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "data")
    output_file_places = os.path.join(output_dir, f"fsq_places_sample_{num_samples}.csv")
    output_file_categories = os.path.join(output_dir, "fsq_categories_sample.csv")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    counter = 0

    with open(output_file_places, 'w', newline='', encoding='utf-8') as f:
        # the load_dataset function is called within the context manager to close the connection automatically
        ds_places = load_dataset("foursquare/fsq-os-places", name="places", streaming=True, split=f"train")
        writer = csv.DictWriter(f, fieldnames=ds_places.column_names) # type: ignore
        writer.writeheader()

        for row in tqdm(ds_places, total=num_samples, desc="Writing places dataset"):
            counter += 1

            if counter >= num_samples:
                break

            writer.writerow(row)

    if os.path.exists(output_file_categories):
        print(f"Categories dataset already exists at {output_file_categories}")
        return

    with open(output_file_categories, 'w', newline='', encoding='utf-8') as f:
        print("Writing categories dataset...")
        ds_categories = load_dataset("foursquare/fsq-os-places", name="categories", streaming=True, split=f"train")
        writer = csv.DictWriter(f, fieldnames=ds_categories.column_names) # type: ignore
        writer.writeheader()
        
        for row in tqdm(ds_categories, desc="Writing categories dataset"):
            writer.writerow(row)



if __name__ == "__main__": 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_samples", type=int, default=100000)
    args = parser.parse_args()  
    load_dataset_way1(args.num_samples)
