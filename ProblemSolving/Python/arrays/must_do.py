"""
This script contains my solutions for curated arrays problems on GFG
"""


import random
from collections import Counter
random.seed(0)



# starting with: https://www.geeksforgeeks.org/problems/peak-element/1?page=1&sprint=50746f92a895c22a50504ac0c1fb9c84&sortBy=submissions
def _peakElement(arr, low, high):
    # first check the border cases
    if arr[low] >= arr[low + 1]:
        return low
    
    if arr[high] >= arr[high - 1]:
        return high

    mid = (low + high) // 2
    # check if mid is a peak
    if arr[mid] >= arr[mid + 1] and arr[mid] >= arr[mid - 1]:
        return mid
    
    if arr[mid - 1] >= arr[mid]:
        return _peakElement(arr, low, mid - 1)
    
    return _peakElement(arr, mid + 1, high)
 
def peakElement(arr, n):
    if n == 1:
        return 0
    return _peakElement(arr, 0, n - 1)

def isSubset( a1, a2, n=None, m=None):
    c1, c2 = Counter(a1), Counter(a2)
    for k, v in c2.items():
        if k not in c1:
            return False
        if v > c1[k]:
            return False
    return True



## this one is tough: 
## https://www.geeksforgeeks.org/problems/minimum-number-of-jumps-1587115620/1?page=1&difficulty=Medium&status=unsolved&sprint=50746f92a895c22a50504ac0c1fb9c84&sortBy=submissions 
def minJumps(arr, n = None):
    if n is None:
        n = len(arr)
    count = 1
    index = 0
    current_limit = arr[0]

    if current_limit >= n - 1:
        return 1

    while index < n:
        next_limit = current_limit
        
        while index <= current_limit:
            next_limit = max(next_limit, arr[index] + index)
            next_limit = min(next_limit, n - 1)
            index += 1
    
        if index == n:
            return count

        if next_limit == current_limit:
            # this means, it is not possible to move further
            return -1

        current_limit = next_limit
        count += 1
    
    return count

def minJumpsNaive(arr, index = 0, memo=None):
    n = len(arr)
    if index == len(arr) - 1:
        return 1
    if index + arr[index] >= n - 1:
        return 1

    if arr[index] == 0:
        return -1
    if memo is None:
        memo = {}

    if index in memo:
        return memo[index]

    v = None
    for i in range(1, arr[index] + 1):
        t = minJumpsNaive(arr, index + i, memo=memo)
        if t != -1:
            v = t if v is None else min(v, t)
    
    if v is None:
        memo[index] = -1
    else:
        memo[index] = 1 + v

    return memo[index]
