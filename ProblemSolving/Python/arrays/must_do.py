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

import random
random.seed(0)

def random_array(n:int):
    return [random.randint(0, 100) for _ in range(n)]


if __name__ == "__main__":
    for _ in range(1000):
        n = random.randint(1, 10 ** 5)
        arr = random_array(n)
        s = random.randint(0, 10 ** 6)
        # correct = subArraySumNaive(arr, s)
        mine = subArraySum(arr, s)
        
        if mine[0] != -1:
            assert sum(arr[mine[0] - 1: mine[1]]) == s, "the sum isn't summing"

        # if correct[0] != -1:
        #     assert sum(arr[correct[0] - 1: correct[1]]) == s, "the sum isn't summing"

        # assert correct == mine, "code isn't correct"
