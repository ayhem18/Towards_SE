from typing import List
from graphs import neetcode as nc
from hashing.test_hash import test_first_not_repeat_char
from hashing.gfg1 import findLongestConseqSubseq, getPairsCount, firstRepeated, maxLen,canPair, encode, decode

if __name__ == '__main__':
    strs = ["", "", "  "]
    o = decode(encode(strs))
    print(strs == o)
