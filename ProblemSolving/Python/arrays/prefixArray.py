"""
This script contains problems solved with the prefix array technique.
"""

from typing import List, Union
from collections import defaultdict

def prefixSum(arr: List) -> Union[float, int]:
    # the variable to save the sum at each point
    s = 0
    
    # the array
    acc_sum = [0 for _ in arr]

    # the loop to save the accumulative sums
    for index, v in enumerate(arr):
        s += v
        acc_sum[index] = s

    return acc_sum        
        

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
                return [real_index + 2, i1 + 1]
            
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


def longSubarrWthSumDivByK (arr: list[int],  n: int, K) : 
    """
    https://www.geeksforgeeks.org/problems/longest-subarray-with-sum-divisible-by-k1259/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article 
    """

    total = 0
    prefixSum = arr.copy()
    for i, v in enumerate(arr):
        total += v
        prefixSum[i] = (total % K)

    max_len = -1
    for i, v in enumerate(prefixSum):
        if v == 0:
            max_len = i + 1
    
    # if the entire array has a sum divisible by 'K', then return already
    if max_len == n:
        return n

    mods_indices = {}
    for i, v in enumerate(prefixSum):
        if v in mods_indices:
            mods_indices[v][1] = i
        else:
            mods_indices[v] = [i, -1]

    for _, pair in mods_indices.items():
        if pair[1] != -1:
            max_len = max(max_len, pair[1] - pair[0])

    return max_len

# this problem can be converted into the famous problem: 
# find the number of subarrays with zero sum

# https://www.geeksforgeeks.org/problems/count-subarrays-with-equal-number-of-1s-and-0s-1587115620/1
def countSubarrWithEqualZeroAndOne(arr, n = None):
    if n is None:
        n = len(arr)

    # first convert 0s to -1
    for i in range(n):
        if arr[i] == 0:
            arr[i] = -1

    acc_sum_array = [0 for _ in range(n)]
    ac_sum = 0

    ac_sum_map = {}

    for j in range(n):
        ac_sum += arr[j]
        acc_sum_array[j] = ac_sum 

        if ac_sum not in ac_sum_map:
            ac_sum_map[ac_sum] = 0 

        ac_sum_map[ac_sum] += 1

    res = 0

    # now we have all the values
    for s in acc_sum_array:
        res += int(s == 0) 
    
    for _, v in ac_sum_map.items():        
        res += (v * (v- 1)) // 2

    return res


# https://www.geeksforgeeks.org/problems/longest-span-with-same-sum-in-two-binary-arrays5142/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
def longestCommonSum(arr1: List[int], arr2: List[int]) -> int:
    # I did not use the fact that arr1 and arr2 are binary which is slightly worrying me but still, why not...
    accsum1 = prefixSum(arr1)
    accsum2 = prefixSum(arr2)

    max_span = 0

    for i, (v1, v2) in enumerate(zip(accsum1, accsum2)):
        if v1 == v2:
            max_span = i + 1

    diff_hash = defaultdict(lambda : [])

    for index, (v1, v2) in enumerate(zip(accsum1, accsum2)):
        d = v1 - v2
        if d not in diff_hash or len(diff_hash[d]) == 1:
            diff_hash[d].append(index)
        else:
            diff_hash[d][-1] = index

    # iterate through the differences hashmap    
    res = 0
    for _, indices in diff_hash.items():
        if len(indices) == 2:
            res = max(indices[1] - indices[0], res) 

    return max(max_span, res)
