import os
import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText

from solution_step1 import Place, PlaceCsvParser, PlaceCsvFormatter, PlaceFilter

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

    # create a pipeline
    with beam.Pipeline() as pipeline:
        formatted_data = (pipeline
         | "Read from CSV" >> ReadFromText(input_file, skip_header_lines=1)
         | "Parse CSV" >> beam.ParDo(PlaceCsvParser(header=header))
        #  | "Format CSV" >> beam.ParDo(PlaceCsvFormatter())
        )

        # filter the places by the country
        prepared_data = (formatted_data
            | "Filter" >> beam.ParDo(PlaceFilter(country_codes=["US", "CA", "DE", "UK"]))
            | "Format CSV" >> beam.ParDo(PlaceCsvFormatter())
        )

        # Reshuffle pattern to force a single worker for the output
        # this is a hack to improve performance: called the Reshuffle pattern (the understanding is still very vague, needs to dive deeper into distributed processing principles)
        _ = (prepared_data
            | 'Add Dummy Key' >> beam.Map(lambda x: (None, x))
            | 'Group by Key' >> beam.GroupByKey()
            | 'Ungroup' >> beam.FlatMap(lambda kv: kv[1])
            | "Write to CSV" >> WriteToText(
                output_file,
                file_name_suffix='.csv',
                header=",".join(Place._fields),
                num_shards=1,
                shard_name_template=''
              )
        )


if __name__ == "__main__":
    main()