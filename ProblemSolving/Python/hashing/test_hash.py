"""
This script contains tests I wrote for problems that are not tested on any online platform: the idea is to
generate random input and compare the output of a naive (unoptimized) version with the optimized one. 
"""
import random
random.seed(69)

from tqdm import tqdm

from .gfg1 import first_not_repeat_char_1_traversal, first_not_repeat_char_2_traversals

def generate_random_string(str_len: int) -> str:
    return "".join([chr(ord('a') + random.randint(0, 25)) for _ in range(str_len)])

def test_first_not_repeat_char(num_tests:int = 10 ** 5):
    n = random.randint(1, 1000)
    string = generate_random_string(str_len=n)    
    for _ in tqdm(range(num_tests), desc='testing !!!'):
        o1, o2 = first_not_repeat_char_1_traversal(string), first_not_repeat_char_2_traversals(string)
        assert o1 == o2, f"The code breaks for the string {string}"

    print("ALL TESTS PASSED !!!")
