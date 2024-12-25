"""
This script contains my solutions to problems based on sorting the array.
"""

from typing import List

# https://www.geeksforgeeks.org/problems/rearrange-array-such-that-even-positioned-are-greater-than-odd4804/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

# the main idea of this problem is as follows: let k = n // 2, spread the largest k numbers on the odd cells and the rest on the even cells: the condition will be satisfied.
def rearrangeArray(arr: List[int]):
    sorted_arr = sorted(arr)
    
    n = len(arr)
    
    new_arr = [0 for _ in range(n)]

    for i in range(1, n, 2):
        new_arr[i] =  sorted_arr[n - 1 - i // 2]

    for i in range(0, n, 2):
        new_arr[i] = sorted_arr[i // 2]

    return new_arr


def findMinDiff(arr: List[int], m:int):
    # for the subset of "m" numbers to have minimal difference (between maximum and minimum)
    # the element have to be sorted
    # then simply sort, and then consider all subarrays of length "m"
    # return the minimum difference
    min_diff = float("inf")
    a = sorted(arr)
    n = len(a)

    for i, v in enumerate(a):
        if i + m - 1 >= n:
            break 

        min_diff = min(a[i + m - 1] - v, min_diff)

    return min_diff



# https://www.geeksforgeeks.org/problems/kth-smallest-element5635/1?page=1&category=Arrays&difficulty=Medium&status=unsolved&sortBy=submissions
# this problem uses a very specific idea: basic O(n) sorting using extra memory. Such an approach is only applicable to scenarios where the range of data is known in advance
# and can fit into memory.

def kthSmallest(array: List[List[int]], k: int) -> int:
    # find the maximum element in the array
    max_element = -float("inf")
    
    # find the maximum element
    for v in array: 
        max_element = max(max_element, v)
    
    # an array to save whether an element exists in the array
    memory_bank = [0 for _ in range(max_element + 1)]
    
    for v in array: 
        memory_bank[v] = 1

    counter, i = 0, 1

    while i < max_element + 1:
        counter += int(memory_bank[i] == 1)
        
        if counter == k:
            return i
        
        i += 1

    return i - 1
