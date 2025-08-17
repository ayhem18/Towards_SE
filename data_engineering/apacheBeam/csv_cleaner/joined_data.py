"""
This script contains functions to format to worked with the joined data: places + categories
"""

from typing import Dict, NamedTuple, Iterable, Sequence, Tuple

from place import Place, PlaceCsvFormatter

class PlaceWithCategory(NamedTuple):
    """
    This class represents a place with its category
    """
    place: Place
    categories: Sequence[str]


def flatten_joined_data(element: Tuple[str, Dict[str, Iterable]]) -> Iterable[Tuple[str, Tuple[Place, str]]]:
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
        yield (place.fsq_place_id, (place, category_name))
    

def map_to_place_with_categories(element: Tuple[str, Iterable[Tuple[Place, str]]]) -> PlaceWithCategory:
    """
    Basically an element if of the form:
    (place_id, [(place, category1), (place, category2), ... (place, category_n)])
    hence, first extract the iterable of tuples, extract one instance of the place
    and then extract the categories from the iterable of tuples
    """
    _, iterable_of_tuples = element
    place = list(iterable_of_tuples)[0][0]
    categories = [category for (_, category) in iterable_of_tuples]
    return PlaceWithCategory(place, categories)





class PlaceWithCategoryCsvFormatter(PlaceCsvFormatter):
    """
    Format a PlaceWithCategory object to a csv string
    """
    def __init__(self, fields_to_exclude: Sequence[str] = []):
        super().__init__(fields_to_exclude=fields_to_exclude)
        

    def process(self, element: PlaceWithCategory) -> Iterable[str]:
        """
        Format a PlaceWithCategory object to a csv string
        """
        # extract the place and the categories
        place, categories = element

        # super().process returns an iterable (with only one element: the csv string representation of the place)
        place_processed = list(super().process(place))[0]

        categories_str = '_'.join(categories)

        final_str = ','.join([place_processed, categories_str])
        yield final_str


    @classmethod
    def get_header(cls, fields_to_exclude: Sequence[str] = []) -> str:
        """
        Get the header for the csv file
        """
        fields2exclude = set(fields_to_exclude)
        fields = [f for f in Place._fields if f not in fields2exclude] + ['categories']
        return ','.join(fields)

