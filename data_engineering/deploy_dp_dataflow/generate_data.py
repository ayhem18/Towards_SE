import json
import os
import random
from string import ascii_lowercase


POSSIBLE_KEYS = [f"key_{i}" for i in range(1, 11)] # 10 keys

def get_random_dictionary():
    length = 3
    val = "_".join([random.choice(ascii_lowercase) for _ in range(length)])
    key = random.choice(POSSIBLE_KEYS)
    return {key: val}


def generate_data(num_samples: int):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    for sample_index in range(1, num_samples + 1):
        random_dict = get_random_dictionary()
        with open(os.path.join(data_dir, f"data_{sample_index}.json"), "w") as f:
            json.dump(random_dict, f)



if __name__ == "__main__":
    generate_data(100)
