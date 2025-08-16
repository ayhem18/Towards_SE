"""
This script is a solution to the very first formulation of the four square dataset processing pipeline.


1. read data from the csv files (understand how to do that properly)
2. Possibly define schemas: which fields to keep and which to discard
3. Filter rows rows whose "name" column consists only of english letters, spaces and numbers
5. Filter by country code (US, CA, DE, UK)
4. load the categories dataset
5. join both datasets on the fsq_cateogies_ids column
6. use the category name to filter restaurants
7. save the results to a new csv file
"""


# create a schema for the places dataset: 


import csv
import datetime

import apache_beam as beam

from typing import Iterable, NamedTuple, Optional, Sequence

class Place(NamedTuple):
    """
    The Place schema discards the following fields: 

    'fsq_place_id', 
    'latitude', 
    'longitude', 
    'address', 
    'locality',
    'region', 
    'postcode', 
    'admin_region', 
    'post_town', 
    'po_box', 
    'date_refreshed', 
    'date_closed', 
    'facebook_id', 
    'twitter', 
    'fsq_category_labels', 
    'placemaker_url', 
    'unresolved_flags', 
    'geom',
    'bbox'

    keeping only: 
    'name', -- to filter by the name (keep only names with specific patterns)
    'country', -- to filter by the country (keep only places in the US, CA, DE, UK)
    'date_created', -- to filter by the age of the place
    'date_closed', -- to make sure the place is still open
    'tel',  -- keep only places with a phone number
    'website', -- keep only places with a website
    'email', -- keep only places with an email
    'instagram', -- keep only places with an instagram
    'fsq_category_ids', -- to filter by the category (to be joined with the categories dataset and filtered by the category name)
    """

    name: str
    country: str
    date_created: Optional[datetime.datetime]
    date_closed: Optional[datetime.datetime]
    tel: Optional[str]
    website: Optional[str]
    email: Optional[str]  
    instagram: Optional[str]
    fsq_category_ids: Sequence[str]


class PlaceCsvParser(beam.DoFn):

    def __init__(self, header: Sequence[str]):
        self.header = header


    def process(self, element: str) -> Iterable[Place]:
        """Element is expected to be a line (the csv file is read by lines)

        NOTE: the type hinting is extremely important here !!! at the time of writing this comment, the pipeline was basically: 
        1. read csv file
        2. parse the csv file
        3. write the parsed data 
        with a return type different from Iterable, the pipeline raises an error immediately (maybe not setting one could work, but that's not ideal)       
        The WriteToText transform might expect an iterable (need to understand how to find this information about each transformation and how to inspect this)

        Args:
            element (str): a line from the csv file

        Returns:
            Iterable[Place]: a Place object
        """

        try:
            # first use csv reader 
            element_as_row = next(csv.reader([element]))

            if len(element_as_row) != len(self.header):
                raise ValueError(f"Row has {len(element_as_row)} columns, but expected {len(self.header)}")
            
            record = dict(zip(self.header, element_as_row))

            yield Place(
                name=record['name'], # type: ignore
                country=record['country'], # type: ignore
                date_created=record['date_created'], # type: ignore
                date_closed=record['date_closed'], # type: ignore
                tel=record['tel'], # type: ignore
                website=record['website'], # type: ignore
                email=record['email'], # type: ignore
                instagram=record['instagram'], # type: ignore
                fsq_category_ids=record['fsq_category_ids'], # type: ignore
            )

        except Exception as e:
            # let's keep it simple for now
            pass               



class PlaceCsvFormatter(beam.DoFn):
    """
    At the time of writing this class, I am using the readToText function to write the data to a text file.
    I am not sure if there is a better way to do this...
    """

    def process(self, element: Place) -> Iterable[str]:
        """
        convert the Place object to a its csv string representation

        Args:
            element (Place): a Place object
        Returns:

            Iterable[str]: a csv string representation of the Place object
        """
        fields = element._asdict()
        fields_as_list = list(fields.values())
        yield ','.join(fields_as_list)

