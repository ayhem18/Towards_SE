from typing import List
import random
random.seed(69)

def generate_random_string(str_len: int) -> str:
    return "".join([chr(ord('a') + random.randint(0, 25)) for _ in range(str_len)])

def print_2d_array(a: List[List]):
    for row in a:
        r = [str(e) for e in row]
        print(" ".join(r))
