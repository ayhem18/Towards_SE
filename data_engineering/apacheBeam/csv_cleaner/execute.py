import os

import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText

from place import PlaceCsvParser, PlaceFilter
from category import CategoryCsvParser, CategoryFilter
from joined_data import PlaceWithCategoryCsvFormatter, flatten_joined_data, map_to_place_with_categories


def execute_pipeline():

    # prepare input, output files and headers
    script_dir = os.path.dirname(os.path.abspath(__file__))
    places_input_file = os.path.join(script_dir, "data", "fsq_places_sample_100000.csv")
    categories_input_file = os.path.join(script_dir, "data", "fsq_categories_sample.csv")
    output_file = os.path.join(script_dir, "data", "joined_places_and_categories")

    places_header = ['fsq_place_id', 'name', 'latitude', 'longitude', 'address', 'locality',
       'region', 'postcode', 'admin_region', 'post_town', 'po_box', 'country',
       'date_created', 'date_refreshed', 'date_closed', 'tel', 'website',
       'email', 'facebook_id', 'instagram', 'twitter', 'fsq_category_ids',
       'fsq_category_labels', 'placemaker_url', 'unresolved_flags', 'geom',
       'bbox']

    category_header = ['category_id', 'name', 'parents', 'hierarchy']

    category_key_words = ["restaurant", "cafe", "bar", "pub", "hotel", "motel", "inn", "resort", "lodging"]


    # time to create the pipeline !!!
    
    pipeline = beam.Pipeline()

    places = (pipeline
        | "Read Places from CSV" >> ReadFromText(places_input_file, skip_header_lines=1)
        | "Parse Places CSV" >> beam.ParDo(PlaceCsvParser(header=places_header))
        | "Filter Places" >> beam.ParDo(PlaceFilter(country_codes=["US", "CA", "DE", "UK"]))
    )

    # read the categories, parse and filter 
    categories = (pipeline 
            | "Read Categories from CSV" >> ReadFromText(categories_input_file, skip_header_lines=1) 
            | "Parse Categories CSV" >> beam.ParDo(CategoryCsvParser(header=category_header))
            | "Filter Categories" >> beam.ParDo(CategoryFilter(category_key_words=category_key_words))
    )

    # at this point the 'places' collection contains elements of type Place
    # type Place contains a field called 'category_ids' which is a list of category ids (string objects)

    # each place should be converted into multiple instances (because otherwise we cannot perform the join operation with the categories collection)
    # let's reason about this for a moment: the join operation requires 2 collections with a where each element is a pair (key, value)
    # since we will join on the category_id field, we need to convert each place into multiple (cat_id, place) pairs
    # and similarly for the categories collection, we need to convert each category into a (cat_id, cat_name) pair

    # flatmap takes a place and generates multiple (cat_id, place) pairs and then flattens them into a single collection
    places_kv = (
        places 
        | 'Map Places to (cat_id, place)' >> beam.FlatMap(
            lambda place: [(cat_id, place) for cat_id in place.category_ids] # any place with no category_ids was filtered in a previous step
        )
    )

    categories_kv = (
        categories
        | 'Map Categories to (cat_id, cat_name)' >> beam.Map(lambda cat_object: (cat_object.category_id, cat_object.category_name))
    )


    # the join operation expects either 2 collections or a map where "values" are collections, it is important to note 

    joined_data = (
        {'places': places_kv, 'categories': categories_kv}
        | 'Join Places and Categories' >> beam.CoGroupByKey()
    )


    # after checking the "https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.CoGroupByKey"
    # it seems that the output will be of the form: 
    # [
    # (cat_id1, {places: [place1, place2 ...], categories: [cat_id1_name]}), 
    # (cat_id2, {places: [place1, place2 ...], categories: [cat_id2_name]}), 
    # ...
    #]
    
    # the final goal is to have a collection where each element is has the schema (Place + all categories)
    # to do that, we need to reach the intermediate form: 

    # [Place: [cat_name1, cat_name2, ...]] 

    # to reach this form, we need to flatten the joined data and then apply a groupByKey operation (where place is the key)
    
    _ = (
        joined_data | 'Flatten Joined Data' >> beam.FlatMap(flatten_joined_data) 
        | 'Group by Place' >> beam.GroupByKey() 
        | 'Map to PlaceWithCategory' >> beam.Map(map_to_place_with_categories)
        | 'Format PlaceWithCategory' >> beam.ParDo(PlaceWithCategoryCsvFormatter())
        | 'Write to CSV' >> WriteToText(output_file, file_name_suffix='.csv', 
        header=PlaceWithCategoryCsvFormatter.get_header(), 
        num_shards=1, 
        shard_name_template=''
        )
    )


    pipeline.run()


def main():


    # # create a pipeline
    # with beam.Pipeline() as pipeline:


    #     # Step 2 & 3: Prepare PCollections for Join
    #     # Places have a one-to-many relationship with categories, so we must "explode" them.

    #     # Step 4: Execute the CoGroupByKey join
    #     joined_data = (
    #         {'places': places_kv, 'categories': categories_kv}
    #         | 'Join Places and Categories' >> beam.CoGroupByKey()
    #     )

    #     # Step 5: Process the joined results to re-key by Place object
    #     def invert_to_place_key(element):
    #         (_cat_id, data) = element
    #         if not data['places'] or not data['categories']:
    #             return  # This makes it an INNER JOIN

    #         category_name = data['categories'][0]
    #         for place in data['places']:
    #             yield (place, category_name)

    #     place_to_category_pairs = (
    #         joined_data
    #         | 'Invert to Place Key' >> beam.FlatMap(invert_to_place_key)
    #     )

    #     # Step 6: Group by Place to aggregate all categories
    #     grouped_by_place = (
    #         place_to_category_pairs
    #         | 'Group by Place' >> beam.GroupByKey()
    #     )
        
    #     # Step 7: Format the final, aggregated output
    #     def format_final_output(element):
    #         (place, category_names) = element
    #         # Remove duplicate category names that might arise from the join
    #         unique_categories = sorted(list(set(category_names)))
    #         return f"Place: {place.name} ({place.country}) | Categories: {', '.join(unique_categories)}"

    #     formatted_results = (
    #         grouped_by_place
    #         | 'Format Final Output' >> beam.Map(format_final_output)
    #     )

    #     # Write the final results to a text file
    #     _ = (
    #         formatted_results
    #         | 'Write Results' >> WriteToText(output_file, file_name_suffix='.txt')
    #     )

    execute_pipeline()

if __name__ == "__main__":
    main()