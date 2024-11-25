"""
This file contains my solutions for some problems on 'arrays'
"""
from math_utils import greatest_common_divisor
from utils import random_array

import math

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



# this problem is the reason, I am considering studying Number Theory once again
# rotate an array with any K using O(1) space
def rotate_constant_space(array: list, k: int):
    n = len(array)
    k = k % n

    if n == 0 or k == 0:
        return

    gcd = greatest_common_divisor(n, k)

    saved_element = array[0]

    if gcd == 1:
        # if the greatest commond divisor between n and k is 1, then the elements will not collide        
        counter = 0
        index = k
        
        while counter < n:
            temp = array[index]
            array[index] = saved_element
            saved_element = temp
            index = (index + k) % n
            counter += 1         

        return     

    # gcd > 1
    for reminder in range(0, gcd):

        max_counter =  n // gcd
        counter = 0

        index = (reminder + k) % n
        saved_element = array[reminder]
        
        while counter < max_counter:
            temp = array[index]
            array[index] = saved_element
            saved_element = temp
            index = (index + k) % n
            counter += 1
            
def rotate_linear_space(array: list, k:int):
    n = len(array)
    new_array = [0 for _ in array]

    for i in range(len(array)):
        new_array[(i + k) % n] = array[i]

    return new_array        

    