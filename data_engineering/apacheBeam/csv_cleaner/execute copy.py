import os
import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText
import ast
from place import Place, PlaceCsvParser, PlaceCsvFormatter, PlaceFilter
from category import Category, CategoryCsvParser, CategoryCsvFormatter, CategoryFilter

def main():
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


    # create a pipeline
    with beam.Pipeline() as pipeline:
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

        # Step 2 & 3: Prepare PCollections for Join
        # Places have a one-to-many relationship with categories, so we must "explode" them.
        places_kv = (
            places 
            | 'Key Places by Category ID' >> beam.FlatMap(
                lambda place: [(cat_id, place) for cat_id in place.category_ids] # any place with no category_ids was filtered in a previous step
            )
        )

        # Categories are one-to-one, so a simple Map is enough.
        categories_kv = (
            categories
            | 'Key Categories by ID' >> beam.Map(lambda c: (c.category_id, c.category_name))
        )

        # Step 4: Execute the CoGroupByKey join
        joined_data = (
            {'places': places_kv, 'categories': categories_kv}
            | 'Join Places and Categories' >> beam.CoGroupByKey()
        )

        # Step 5: Process the joined results to re-key by Place object
        def invert_to_place_key(element):
            (_cat_id, data) = element
            if not data['places'] or not data['categories']:
                return  # This makes it an INNER JOIN

            category_name = data['categories'][0]
            for place in data['places']:
                yield (place, category_name)

        place_to_category_pairs = (
            joined_data
            | 'Invert to Place Key' >> beam.FlatMap(invert_to_place_key)
        )

        # Step 6: Group by Place to aggregate all categories
        grouped_by_place = (
            place_to_category_pairs
            | 'Group by Place' >> beam.GroupByKey()
        )
        
        # Step 7: Format the final, aggregated output
        def format_final_output(element):
            (place, category_names) = element
            # Remove duplicate category names that might arise from the join
            unique_categories = sorted(list(set(category_names)))
            return f"Place: {place.name} ({place.country}) | Categories: {', '.join(unique_categories)}"

        formatted_results = (
            grouped_by_place
            | 'Format Final Output' >> beam.Map(format_final_output)
        )

        # Write the final results to a text file
        _ = (
            formatted_results
            | 'Write Results' >> WriteToText(output_file, file_name_suffix='.txt')
        )


if __name__ == "__main__":
    main()