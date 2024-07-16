from typing import List
from graphs import neetcode as nc
from hashing.test_hash import test_first_not_repeat_char
from hashing.gfg1 import findLongestConseqSubseq, getPairsCount, firstRepeated, maxLen,canPair, encode, decode
from twoPointers.Tpnts2 import maxArea, trap

from slidingWindow.sw1 import longestUniqueSubsttr, countDistinct

if __name__ == '__main__':
    a = [1, 2, 3, 4, 5, 6]
    for k in range(1, len(a) + 1):
        print(f"k:{k}, count: {countDistinct(arr=a, n=len(a), k=k)}")

