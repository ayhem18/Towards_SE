import os,json,re
import apache_beam as beam

from typing import Dict, Iterable, List
from apache_beam import Pipeline, Map 
from apache_beam.io import ReadFromText, WriteToText, ReadFromJson, WriteToJson
from apache_beam.options.pipeline_options import PipelineOptions



def get_data_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'data')

def read_write():
    data_dir = get_data_dir()
    input_file = os.path.join(data_dir, 'input.txt')
    output_file = os.path.join(data_dir, 'output.txt')

    with Pipeline() as pip:
        output = (pip 
            | "Read" >> ReadFromText(input_file) # Read the input file
            | "Write" >> WriteToText(output_file) # Write the output file
            )

    # something is weird about this pipeline, since the file name contained additional tags... (output.txt-00000-of-00001) ??

def read_write_count():
    data_dir = get_data_dir()
    input_file = os.path.join(data_dir, 'input.txt')
    output_file = os.path.join(data_dir, 'output_with_count.txt')

    # need to investigate the difference between standard pipeline declaration and pipeline with context manager
    # with context manager, no need to call the run() method...
    pip = Pipeline()
    output = (pip 

        | "Read" >> ReadFromText(input_file) # Read the input file
        | "Count characters in line" >> Map(lambda line: f"{line} : has {len(line)} characters") # Count the number of characters in each line
        | "Write" >> WriteToText(output_file) # Write the output file
        )

    pip.run()


# let's spice up things a bit: read data from a json file, filter elements and write the new json file

class FilterJson(beam.DoFn):
    def process(self, element: Dict) -> Iterable[Dict]:
        if element['age'] > 30:
            c = element.copy()
            c.pop('age')
            yield c



def read_json_and_map():
    data_dir = get_data_dir()
    input_file = os.path.join(data_dir, 'input_json.txt')
    output_file = os.path.join(data_dir, 'output_json_filtered.json')
        
    pip = Pipeline()

    json_output = (pip | "Read" >> ReadFromText(input_file)
    | "convert to dict" >> Map(lambda x: json.loads(x)) # as I understand: each element in a line: a textual representation of json object: needs to be converted explicitly
    | "Filter by age" >> beam.ParDo(FilterJson())
    | "Write" >> WriteToText(output_file)    
    )

    pip.run()


def read_text_and_word_count():
    data_dir = get_data_dir()

    input_file = os.path.join(data_dir, 'input.txt')
    output_file = os.path.join(data_dir, 'output_word_count.txt')

    pip = Pipeline()

    # most errors come from type schemas... Learn how to debug schemas..

    output = (pip
    | "Read" >> ReadFromText(input_file)
    | "Split" >> beam.FlatMap(lambda line: re.split("[^a-zA-Z]+", line)) # the function must accept a single element and return an iterable
    | "Create key-value pairs" >> beam.Map(lambda word: (word, 1)) # apparently, the GroupByKey() function expects a PCollection where each element is a tuple of 2 elements: (key, value) 
    | "Group" >> beam.GroupByKey() # group by key: word
    | "Count" >> beam.Map(lambda pair: (pair[0], len(list(pair[1])))) # count the number of words
    | "Write" >> WriteToText(output_file)
    )

    pip.run()




def make_json_in_lines():
    data_dir = get_data_dir()
    input_file = os.path.join(data_dir, 'input.json')

    with open(input_file, 'r') as f:
        data = json.load(f)

    with open(input_file, 'w') as f:
        json.dump(data,f, indent=1)


def main():
    read_text_and_word_count()

if __name__ == "__main__":
    main()