"""
This script builds an Apache Beam pipeline to analyze the Foursquare Places dataset.
It identifies and counts the number of locations for restaurant chains in the United States.
"""
import os
import csv
import ast  # Used for safely evaluating string-formatted lists
import apache_beam as beam
from typing import Iterable, Dict, Tuple
from apache_beam.io import ReadFromText, WriteToText

class ParsePlaceData(beam.DoFn):
    def process(self, element: str) -> Iterable[Dict]:
        """
        Parses a single row from the Foursquare CSV and yields a dictionary.
        """
        try:
            row = next(csv.reader([element]))
            # The header can be inferred from the dataset page or the CSV header itself
            header = [
                "fsq_id", "location", "country", "postcode", "region", "locality",
                "address", "latitude", "longitude", "category_ids", "category_labels",
                "chain_id", "name"
            ]
            
            if len(row) != len(header):
                return
            
            record = dict(zip(header, row))
            yield record
        except Exception:
            pass

class FilterUSRestaurants(beam.DoFn):
    def process(self, element: Dict) -> Iterable[Dict]:
        """
        Filters for records that are restaurants located in the US.
        """
        try:
            if element['country'] == 'US':
                # The category_labels field is a string representation of a list.
                # We use ast.literal_eval to safely parse it into a Python list.
                labels = ast.literal_eval(element['category_labels'])
                if any("Restaurant" in label for label in labels):
                    yield element
        except (ValueError, SyntaxError):
            # Ignore records with malformed category_labels
            pass

def create_pipeline(input_file: str, output_file: str):
    """
    Creates and runs the Foursquare data analysis pipeline.
    """
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | 'Read CSV' >> ReadFromText(input_file, skip_header_lines=1)
            | 'Parse Rows' >> beam.ParDo(ParsePlaceData())
            
            # Requirement 2: Filter for US Restaurants
            | 'Filter US Restaurants' >> beam.ParDo(FilterUSRestaurants())
            
            # Requirement 3: Identify Chains (filter for non-empty chain_id)
            | 'Filter Chains' >> beam.Filter(lambda rec: rec.get('chain_id'))
            
            # Requirement 4: Count Chains
            | 'Map to KV Pairs' >> beam.Map(lambda rec: (rec['chain_id'], 1))
            | 'Count Chains' >> beam.combiners.Count.PerKey()
            
            # Requirement 5: Prepare for Output
            | 'Format Output' >> beam.Map(lambda tpl: f"Chain ID: {tpl[0]}, Locations: {tpl[1]}")
            
            # Requirement 6: Write Output
            | 'Write Results' >> WriteToText(output_file, file_name_suffix='.txt')
        )

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(script_dir, 'data', 'fsq_places_sample.csv')
    output_txt = os.path.join(script_dir, 'data', 'us_restaurant_chains')
    
    # Before running, make sure you have downloaded the sample dataset by running load_ds.py
    if not os.path.exists(input_csv):
        print(f"Error: Input file not found at {input_csv}")
        print("Please run 'python3 load_ds.py' to download the dataset sample first.")
    else:
        create_pipeline(input_csv, output_txt)
        print(f"Pipeline finished. Check the output file starting with: {output_txt}")
