import argparse
import logging
import os
import json
import apache_beam as beam

from datetime import datetime
from apache_beam.pvalue import Row
from apache_beam.io import fileio, WriteToText
from apache_beam.io.avroio import beam_row_to_avro_dict
from apache_beam.options.pipeline_options import PipelineOptions

from mypack.utils import display_message

def create_json_pcollection(pipeline: beam.Pipeline, file_pattern: str):
    """
    Creates a PCollection of parsed JSON objects from a file pattern that can be
    either a local path or a GCS path.

    Args:
        pipeline: The Apache Beam pipeline object.
        file_pattern: A file path pattern, e.g., '/path/to/files/*.json'
                      or 'gs://bucket/path/*.json'.

    Returns:
        A PCollection where each element is a parsed JSON object (dict or list).
    """
    return (
        pipeline
        | 'MatchFiles' >> fileio.MatchFiles(file_pattern)
        | 'ReadMatches' >> fileio.ReadMatches()
        | 'DecodeAndParseJson' >> beam.Map(lambda readable_file: json.loads(readable_file.read().decode('utf-8')))
    )

def extract_key_value(json_obj: dict):
    as_tuple = tuple(list(json_obj.items())[0]) 
    return Row(key=as_tuple[0], value=as_tuple[1])


def write_json_array(pcollection, output_file):
    """Write PCollection as a single JSON array to a file."""
    return (
        pcollection
        | "Combine Into List" >> beam.combiners.ToList()
        | "Convert to JSON Array" >> beam.Map(lambda items: json.dumps([{"key": item.key, "value": item.value} for item in items], indent=2))
        | "Write JSON Array" >> WriteToText(output_file, num_shards=1, shard_name_template='')
    )


def define_pipeline(pipeline: beam.Pipeline, file_pattern: str, output_file: str):
    # different cloud provides, filesystem and so on ...
    # using the file_pattern allows reading files from different sources

    pcoll = create_json_pcollection(pipeline, file_pattern)
    # _ = (pcoll | "Print" >> beam.Map(print))

    result_pcoll = (
        pcoll
        | "Map To Tuple" >> beam.Map(extract_key_value)
        | "Group By Key" >> beam.GroupByKey() 
        | "Count Unique Values" >> beam.Map(lambda x: Row(key=x[0], value=len(set(x[1])))) # Count the number of unique values for each key
    )
    
    # Write as JSON array
    write_json_array(result_pcoll, output_file)

    return pipeline


def run_pipeline(argv: list[str] | None = None):

    parser = argparse.ArgumentParser()  

    # data_bucket_name = os.getenv('DATA_BUCKET_NAME') 
    data_bucket_name = 'ayhem-exp-bucket' #os.getenv('DATA_BUCKET_NAME') 

    if data_bucket_name is None:
        raise ValueError('DATA_BUCKET_NAME is not set')
    
    call_time = datetime.now().strftime('%Y%m%d-%H%M%S')

    file_pattern = f'gs://{data_bucket_name}/data/data_*.json'
    output_path = f'gs://{data_bucket_name}/output/output_{call_time}.json'

    # TODO: define them in a way that accepts arguments
    _, pipeline_options_args = parser.parse_known_args(argv)

    pipeline = beam.Pipeline(options=PipelineOptions(pipeline_options_args))
    
    with pipeline:
        define_pipeline(pipeline, file_pattern, output_path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    display_message()
    run_pipeline()