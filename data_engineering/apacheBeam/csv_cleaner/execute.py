import os
import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText

from place import Place, PlaceCsvParser, PlaceCsvFormatter, PlaceFilter
from category import Category, CategoryCsvParser, CategoryCsvFormatter, CategoryFilter

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "data", "fsq_places_sample_100000.csv")
    output_file = os.path.join(script_dir, "data", "fsq_places_sample_100000_parsed")

    header = ['fsq_place_id', 'name', 'latitude', 'longitude', 'address', 'locality',
       'region', 'postcode', 'admin_region', 'post_town', 'po_box', 'country',
       'date_created', 'date_refreshed', 'date_closed', 'tel', 'website',
       'email', 'facebook_id', 'instagram', 'twitter', 'fsq_category_ids',
       'fsq_category_labels', 'placemaker_url', 'unresolved_flags', 'geom',
       'bbox']

    category_header = ['category_id', 'category_level', 'category_name', 'category_label',
       'level1_category_id', 'level1_category_name', 'level2_category_id',
       'level2_category_name', 'level3_category_id', 'level3_category_name',
       'level4_category_id', 'level4_category_name', 'level5_category_id',
       'level5_category_name', 'level6_category_id', 'level6_category_name']

    category_key_words = ["restaurant", "cafe", "bar", "pub", "hotel", "motel", "inn", "resort", "lodging"]


    # create a pipeline
    with beam.Pipeline() as pipeline:
        places = (pipeline
         | "Read places from CSV" >> ReadFromText(input_file, skip_header_lines=1)
         | "Parse places CSV" >> beam.ParDo(PlaceCsvParser(header=header))
         | "Filter places" >> beam.ParDo(PlaceFilter(country_codes=["US", "CA", "DE", "UK"]))
         | "Format places CSV" >> beam.ParDo(PlaceCsvFormatter())
        )


        # read the categories, parse and filter 
        categories = (pipeline 
                | "Read categories from CSV" >> ReadFromText(input_file, skip_header_lines=1) 
                | "Parse categories CSV" >> beam.ParDo(CategoryCsvParser(header=category_header))
                | "Filter categories" >> beam.ParDo(CategoryFilter(category_key_words=category_key_words))
                | "Format categories CSV" >> beam.ParDo(CategoryCsvFormatter())
        )

        # time to apply a relational join on both datasets on the category_id column
    


        # joined_data = (beam.CoGroupByKey()
        #     | beam.Map(lambda kv: (kv[0], kv[1][0], kv[1][1]))
        # )

        # # Reshuffle pattern to force a single worker for the output
        # # this is a hack to improve performance: called the Reshuffle pattern (the understanding is still very vague, needs to dive deeper into distributed processing principles)
        # _ = (prepared_data
        #     | 'Add Dummy Key' >> beam.Map(lambda x: (None, x))
        #     | 'Group by Key' >> beam.GroupByKey()
        #     | 'Ungroup' >> beam.FlatMap(lambda kv: kv[1])
        #     | "Write to CSV" >> WriteToText(
        #         output_file,
        #         file_name_suffix='.csv',
        #         header=",".join(Place._fields),
        #         num_shards=1,
        #         shard_name_template=''
        #       )
        # )


if __name__ == "__main__":
    main()