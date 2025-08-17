"""
This script contains functions to format to worked with the joined data: places + categories
"""

import apache_beam as beam
from typing import Any, Dict, NamedTuple, Iterable, Sequence, Tuple

from place import Place
from category import Category

class PlaceWithCategory(NamedTuple):
    """
    This class represents a place with its category
    """
    place: Place
    categories: Sequence[str]




def flatten_joined_data(element: Tuple[str, Dict[str, Iterable]]) -> Iterable[Tuple[Place, str]]:
    """
    Flatten the joined data into a list of PlaceWithCategory objects
    """
    _, data = element

    if 'places' not in data or 'categories' not in data:
        raise ValueError(f"Invalid data: {data}")

    places_iterable, categories = data['places'], data['categories'] 

    # if either places or categories are empty, then return
    if len(places_iterable) == 0 or len(categories) == 0: # type: ignore
        return

    if len(categories) != 1: # type: ignore
        raise ValueError(f"Expected 1 category, got {len(categories)}") # type: ignore

    category_name = next(iter(categories)) # type: ignore 

    for place in places_iterable:
        yield (place, category_name)


def map_to_place_with_categories(element: Tuple[Place, Iterable[str]]) -> PlaceWithCategory:
    """
    Map a tuple of (Place, Iterable[str]) to a PlaceWithCategory object
    """
    place, categories = element
    categories_list = list(categories)
    return PlaceWithCategory(place, categories_list)


class PlaceWithCategoryCsvFormatter(beam.DoFn):
    """
    Format a PlaceWithCategory object to a csv string
    """
    def process(self, element: PlaceWithCategory) -> str:
        """
        Format a PlaceWithCategory object to a csv string
        """
        # extract the place and the categories
        place, categories = element

        # ignore the "category_ids" field in the 'place' object
        place_fields = list(place._asdict().values())
        place_fields.remove(place.category_ids)
        categories_str = ','.join(categories)
        return ','.join(place_fields + [categories_str])

    @classmethod
    def get_header(cls) -> str:
        """
        Get the header for the csv file
        """
        fields = list(Place._fields) + ['categories']
        return ','.join(fields)

