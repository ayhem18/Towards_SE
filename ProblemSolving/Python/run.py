from typing import List
from graphs import neetcode as nc
from hashing.test_hash import test_first_not_repeat_char
from hashing.gfg1 import findLongestConseqSubseq, getPairsCount, firstRepeated, maxLen,canPair, encode, decode
from twoPointers.Tpnts2 import maxArea, trap

from slidingWindow.sw1 import smallestSubWithSum
if __name__ == '__main__':
    a = [-2, -2, 0, 1]
    x = -3
    for v in a:
        print(smallestSubWithSum(v, a))
    # print(smallestSubWithSum(x, a))
