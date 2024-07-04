"""
This script contains my solutions for curated arrays problems on GFG
"""


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

from collections import Counter
def isSubset( a1, a2, n=None, m=None):
    c1, c2 = Counter(a1), Counter(a2)
    for k, v in c2.items():
        if k not in c1:
            return False
        if v > c1[k]:
            return False
    return True


# this one is kinda tough !!
# the python version of the same algorithm exceeds the time limit imposed by GFG
# the same algorithm written in C++ passes all tests !!
def subArraySum(arr, n, s):  
    for index, v in enumerate(arr):
        if s == 0 and v == 0:
            return [index + 1, index + 1]
        
    if s == 0:
        return [-1, -1]
    
    # compute the prefix array
    ps = [0 for _ in range(n)]
    cum_sum = 0
    
    for i, v in enumerate(arr):
        cum_sum += v
        ps[i] = cum_sum
    
    # iterate through the cum_sum array 
    for i, cs in enumerate(ps):
        if cs == s:
            return [1, i + 1]        
    
    psi = [-v for v in ps[::-1]]

    # the idea now is to find indices i1, i2 such that ps[i1] + psi[i2] sum up to 's'
    i1, i2 = 0, n - 1
    while i1 < n and i2 >= 0:
        if ps[i1] + psi[i2] > s:
            i2 = i2 - 1

        elif ps[i1] + psi[i2] < s:
            i1 += 1

        else:
            real_index = n - 1 - i2
            
            if real_index <= i1:
                assert sum(arr[real_index + 1: i1 + 1]) == s
                return [real_index + 2, i1 + 1]
            
            assert sum(arr[i1 + 1: real_index + 1]) == s
            return [i1 + 2, real_index + 1]
    
    return [-1, -1]

# this function was written to test the optimized solution
def subArraySumNaive(arr, s, n=None): 
    if n is not None:
        s, n = n, s
    else:
        n = len(arr)

    for i in range(n):
        if arr[i] == s:
            return [i + 1, i + 1]
        for j in range(i, n):
            if sum(arr[i:j + 1]) == s:
                return [i + 1, j + 1]
    return [-1, -1]


def maxSubArraySum(arr):
    """
    https://www.geeksforgeeks.org/problems/kadanes-algorithm-1587115620/1?page=1&difficulty=Medium&status=unsolved&sprint=50746f92a895c22a50504ac0c1fb9c84&sortBy=submissions
    """
    n = len(arr)
    best_sum = -float('inf')
    i, j = 0, 0
    while i < n:
        current = arr[i]
        j = i + 1
        
        best_sum = max(current, best_sum)
        
        while j < n and current >= 0:
            current += arr[j]
            j += 1
            best_sum = max(best_sum, current)

        # set 'i' to 'j'
        i = j

    return best_sum


def maxSubArrayNaive(array):
    best_sum = -float('inf')
    n = len(array)
    for i in range(n):
        for j in range(i, n):
            best_sum = max(best_sum, sum(array[i:j + 1]))
    return best_sum

import random
random.seed(0)

def random_array(n:int, low=0, high=100):
    return [random.randint(low, high) for _ in range(n)]


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


if __name__ == "__main__":
    for i in range(100):
        n = random.randint(5, 1000)
        arr = random_array(n, low=0, high=20)
        s1 = minJumpsNaive(arr)
        s2 = minJumps(arr)
        assert s1 == s2, "yo"        
