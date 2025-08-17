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


import ast
import csv, datetime, re
import apache_beam as beam

from datetime import date
from typing import Any, Iterable, NamedTuple, Optional, Sequence

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
    'fsq_place_id', -- to be used as a primary key
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
    fsq_place_id: str
    name: str
    country: str
    date_created: Optional[date]
    date_closed: Optional[date]
    tel: Optional[str]
    website: Optional[str]
    email: Optional[str]  
    category_ids: Optional[Sequence[str]]


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

            # the types need to be specifically set here: if the next steps rely on the types, the pipeline will fail
            yield Place(
                fsq_place_id=record['fsq_place_id'],
                name=record['name'], 
                country=record['country'],
                date_created=date.fromisoformat(record['date_created']) if record['date_created'] is not None and len(record['date_created']) > 0 else None, 
                date_closed=date.fromisoformat(record['date_closed']) if record['date_closed'] is not None and len(record['date_closed']) > 0 else None, 
                tel=record['tel'], 
                website=record['website'], 
                email=record['email'], 
                category_ids=ast.literal_eval(record['fsq_category_ids']),          # eval is used to convert the string to a list of strings
            )
        
        except Exception as e:
            # let's keep it simple for now
            pass               


class PlaceFilter(beam.DoFn):
    """
    Filter the places by the name
    """

    def __init__(self, country_codes: Sequence[str]):
        self.country_codes = set([c.lower().strip() for c in country_codes])

    def process(self, element: Place) -> Iterable[Place]:
        """
        Filter the places by the name

        Args:
            element (Place): a Place object

        Returns:
            Iterable[Place]: a Place object
        """
        # check the date_closed field
        if element.date_closed is not None:
            return

        # cateogy is is crucial information, if it is not present, the place is not processed
        if element.category_ids is None or len(element.category_ids) == 0:
            return

        # check the country code
        if element.country.lower().strip() not in self.country_codes:
            return

        # # the place must have a phone number, website and an email !! (keep it professional)
        # if (element.name is None or len(element.name) == 0 or 
        #     (element.tel is None or len(element.tel) == 0) or 
        #     (element.website is None or len(element.website) == 0) or 
        #     (element.email is None or len(element.email) == 0)
        #     ):
        #     return

        processed_name = element.name.lower().strip()
        processed_name = re.sub(r'[\s]+', ' ', processed_name)

        # make sure the name is not empty and contains only english letters, spaces and numbers
        if len(processed_name) == 0 or not re.match(r'^[-_?!.,:;a-zA-Z\d\s]+$', processed_name):
            return


        # create a new Place object because modiying the original one is not recommended in the Apache Beam programming guide
        final_element = Place(
            fsq_place_id=element.fsq_place_id,
            name=processed_name,
            country=element.country,
            date_created=element.date_created,
            date_closed=element.date_closed,
            tel=element.tel,
            website=element.website,
            email=element.email,
            category_ids=element.category_ids,
        )

        yield final_element


class PlaceCsvFormatter(beam.DoFn):
    """
    At the time of writing this class, I am using the readToText function to write the data to a text file.
    I am not sure if there is a better way to do this...
    """

    def __init__(self, fields_to_exclude: Sequence[str] = []):
        self.fields_to_exclude = set(fields_to_exclude)

    def _convert_field_to_string(self, field: Any) -> str:
        """
        Convert the field to a string
        """
        if field is None:
            return ""
        
        if isinstance(field, date):
            return field.isoformat()

        # "str" is a sequence, but we don't want to join it !!
        if isinstance(field, Sequence) and not isinstance(field, str):
            return ','.join(field)

        if not isinstance(field, str):
            raise TypeError(f"Field {field} is of type {type(field)}, expected str")

        return field

    def process(self, element: Place) -> Iterable[str]:
        """
        convert the Place object to a its csv string representation

        Args:
            element (Place): a Place object
        Returns:

            Iterable[str]: a csv string representation of the Place object
        """
        fields = [f for k, f in element._asdict().items() if k not in self.fields_to_exclude]

        fields = [self._convert_field_to_string(f) for f in fields]
        
        yield ','.join(fields)


