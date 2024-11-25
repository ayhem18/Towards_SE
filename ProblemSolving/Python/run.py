import random

from typing import List

from tqdm import tqdm
from graphs import neetcode as nc

from hashing.test_hash import test_first_not_repeat_char
from hashing.gfg1 import findLongestConseqSubseq, getPairsCount, firstRepeated, maxLen,canPair, encode, decode
from twoPointers.Tpnts2 import maxArea, trap

from slidingWindow.sw1 import longestUniqueSubsttr, countDistinct, smallestSubWithSum
from div_and_con.dc1 import searchMatrix, findMin
from utils import random_array
from arrays.arrays import rotate_constant_space, rotate_linear_space

def test_constant_space_array_rotation():
    for _ in tqdm(range(1000)):
        n = random.randint(1, 1000)
        # k = random.randint(1, 10 ** 5)

        a = random_array(n, 0, 1000)
        
        for k in range(1, len(a)):
            a_rotated = a.copy()
            rotate_constant_space(a_rotated, k=k)
            a_rotated_correct = rotate_linear_space(a, k=k)

            assert a_rotated_correct == a_rotated, "code doesn't work"

if __name__ == '__main__':
    test_constant_space_array_rotation()