"""
This script contains my solutions for gfg problems that can be solved mainly using a hashmap or a set
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


# https://www.geeksforgeeks.org/problems/array-pair-sum-divisibility-problem3257/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

# 1st check: must have an even number of element 
# save the count of elements with each reminder: {i: {# v | v % k = i }}
# 

def canPair(nums: List[int], k: int):
    if len(nums) % 2 == 1:
        return False
    
    k_nums = [v % k for v in nums]
    
    k_map = dict([(v, 0) for v in k_nums])

    for v in k_nums:
        k_map[v] += 1

    # element divisible by "k" are associated together: need an even count of such numbers
    if 0 in k_map and  k_map[0] % 2 == 1:
        return False

    # if k is even then numbers with reminder k // 2 are grouped together, need an even count of such numbers
    if (k % 2 == 0) and (k // 2) in k_map and (k_map[k // 2] % 2 == 1):
        return False
    
    # for other reminders, then r and k - r need to be grouped together, the total count for each of those reminders must be the same
    for rem, _ in k_map.items():
        other_rem = (k - rem) % k
        
        if (other_rem not in k_map) or (k_map[other_rem] != k_map[rem]):
            return False
        
    return True
    