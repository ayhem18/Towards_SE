"""
This script contains my implementation of some of the "string" problems for "basic" problems in the following GFG list: 
https://www.geeksforgeeks.org/introduction-to-strings-data-structure-and-algorithm-tutorials/ 
"""

def reverseWords(string: str) -> str:
    "https://www.geeksforgeeks.org/problems/reverse-words-in-a-given-string5459/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article"
    words = string.split(".")
    return ".".join(words[::-1])


def findLongestCommonPrefix(s1: str, s2: str) -> str:
    index = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            break
        index +=1 
    return s1[:index]


def longestCommonPrefix(arr, n):
    "https://www.geeksforgeeks.org/problems/longest-common-prefix-in-an-array5129/1"

    if n == 1:
        return arr[0]

    start = findLongestCommonPrefix(arr[0], arr[1])
    
    commonPrefix = start
    for i in range(2, n):
        commonPrefix = findLongestCommonPrefix(commonPrefix, arr[i])
        if len(commonPrefix) == 0:
            return -1
    return commonPrefix

def areIsomorphic(str1: str, str2: str):
    "https://www.geeksforgeeks.org/problems/isomorphic-strings-1587115620/1"
    if len(str1) != len(str2):
        return False
    
    mapping = {}
    mapping_reversed = set()

    for c1, c2 in zip(str1, str2):
        if c1 not in mapping:
            mapping[c1] = c2
            if c2 in mapping_reversed:
                return False
            mapping_reversed.add(c2)
        else:   
            if c2 != mapping[c1]:
                return False

    return True


def isRotated(str1,str2):
    "https://www.geeksforgeeks.org/problems/check-if-string-is-rotated-by-two-places-1587115620/1"
    if len(str1) != len(str2):
        return False
    start = 2
    
    first_rot = True
    for i in range(0, len(str1)):
        if str1[i] != str2[(start + i) % len(str1)]:
            first_rot = False
            break 
    
    if first_rot:
        return True

    start = len(str1) - 2
    for i in range(0, len(str1)):
        if str1[i] != str2[(start + i) % len(str1)]:
            return False
        
    return True


def longest_subseq_polindrome(string: str, freq_map: dict) -> str:
    pass


if __name__ == '__main__':
    s1 = "geeksforgeeks"
    s2 = "geeksgeeksfor"
    # s2 = "abcde"
    print(isRotated(s1, s2))
