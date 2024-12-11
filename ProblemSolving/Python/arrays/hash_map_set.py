"""
This script contains my solutions for gfg problems that can be solved mainly using a hashmap of a set
"""

from typing import List



# https://www.geeksforgeeks.org/problems/smallest-positive-missing-number-1587115621/1?page=1&category=Arrays&difficulty=Medium&status=unsolved&sortBy=submissions
def missingNumber(arr: List[int]) -> int:
    # basically convert all positive numbers into a set and iterate from 1 
    pos_nums_set = set()
    max_element = -float("inf")
    
    for v in arr:
        if v >= 1:
            pos_nums_set.add(v)
        max_element = max(max_element, v)

    # if all element are non-positive, then return 1
    if max_element < 1:
        return 1

    # otherwise iterate from "1" to "max_element + 1", the last number if a guaranteed miss
    for i in range(1, max_element + 2):
        if i not in pos_nums_set:
            return i
    