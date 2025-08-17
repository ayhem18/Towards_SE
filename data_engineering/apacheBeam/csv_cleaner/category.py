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
import csv, datetime, re
import apache_beam as beam

from datetime import date
from typing import Any, Iterable, NamedTuple, Optional, Sequence


class Category(NamedTuple):
    """
    The Category schema discards all the category fields expect the 'category_id' and the 'category_name'
    """
    category_id: str
    category_name: str


class CategoryCsvParser(beam.DoFn):

    def __init__(self, header: Sequence[str]):
        self.header = header


    def process(self, element: str) -> Iterable[Category]:
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
            yield Category(
                category_id=record['category_id'],
                category_name=record['category_name'],
            )

        except Exception as e:
            raise ValueError(f"Error parsing category: {str(e)}")


class CategoryFilter(beam.DoFn):
    """
    Filter the categories by the name
    """

    def __init__(self, category_key_words: Sequence[str]):
        self.category_key_words = set([c.lower().strip() for c in category_key_words])


    def _verify_one_keyword(self, category_name: str, keyword: str) -> bool:
        """
        Check if the category name contains the keyword
        """
        # if the keyword is an expression, then split it    
        words = [w.strip() if len(w.strip()) > 0 else None for w in re.split(r'\s+', keyword)]

        return all((w in category_name) for w in words) # type: ignore # split should not return None...
    

    def process(self, element: Category) -> Iterable[Category]:
        """
        Filter the categories by the name

        Args:
            element (Category): a Category object

        Returns:
            Iterable[Category]: a Category object
        """
        category_name = element.category_name.lower().strip()

        valid_category = False

        for keyword in self.category_key_words:
            if self._verify_one_keyword(category_name, keyword):
                valid_category = True
                break
        
        if valid_category:
            # make sure to return a new category with the processed category name
            yield Category(
                category_id=element.category_id,
                category_name=category_name,
            )



class CategoryCsvFormatter(beam.DoFn):
    """
    At the time of writing this class, I am using the readToText function to write the data to a text file.
    I am not sure if there is a better way to do this...
    """

    def process(self, element: Category) -> Iterable[str]:
        """
        convert the Category object to a its csv string representation

        Args:
            element (Category): a Category object
        Returns:

            Iterable[str]: a csv string representation of the Category object
        """
        fields = [element.category_id, element.category_name]
        yield ','.join(fields)


