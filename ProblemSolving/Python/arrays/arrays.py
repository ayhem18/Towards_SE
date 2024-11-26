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

    
# this problem can be solved in numerous ways; some more efficient than others
# https://www.geeksforgeeks.org/problems/sort-an-array-of-0s-1s-and-2s4231/1

# method1: just save the indices of each value in a dictionary and then populate the array ; O(n) space complexity

# sorting an array with known values can be done in o(1) with extra headache

def sort_array_with_known_elements(array: list, targets: list = None):
    if targets is None:
        targets = [0, 1, 2]

    n = len(array) 
    sorted_array_end = n - 1
    target_value_index = len(targets) - 1

    while target_value_index >= 0:
        target_value = targets[target_value_index]
        temp = sorted_array_end
        
        while temp >= 0 and array[temp] != target_value:
            temp -= 1

        if temp < 0:
            target_value_index -= 1
            continue

        array[temp] = array[sorted_array_end]        
        array[sorted_array_end] = target_value

        # at this point the subarray "array[sorted_array_end:]" is sorted 

        pnt1 = sorted_array_end - 1
        while pnt1 >= 0 and array[pnt1] == target_value:
            pnt1 -= 1

        if pnt1 < 0:
            break 

        # at this point array[pnt1] != target_value and array[pnt1 + 1: ] is sorted
        pnt2 = pnt1

        while pnt2 >= 0:
            while (pnt2 >= 0) and (array[pnt2] != target_value):
                pnt2 -= 1
            
            if pnt2 >= 0:
                # at this point array[pnt2] == target_value
                array[pnt2] = array[pnt1]
                array[pnt1] = target_value
                pnt1 -= 1

        sorted_array_end = pnt1
        target_value_index -= 1
        
    

# this problem is simply another problem in disguise
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


# I am not sure if there is an in-place solution to this problem
def rearrange(arr):
    n = len(arr)
    num_positive = 0
    for v in arr:
        num_positive += int(v >= 0)
    
    min_portion = min(num_positive, n - num_positive)

    new_array = [None for _ in range(n)]

    # populate positive numbers
    index_num, index_arr = 0, 0

    while index_arr < n:
        while index_num < n and arr[index_num] < 0:
            index_num += 1

        if index_num >= n:
            break

        new_array[index_arr] = arr[index_num] 

        index_arr += (2 - int(index_arr >= 2 * min_portion))

        index_num += 1
    

    # populate negative numbers
    index_num, index_arr = 0, int(num_positive > 0)
    while index_arr < n:
        while index_num < n and arr[index_num] >= 0:
            index_num += 1

        if index_num >= n:
            break

        new_array[index_arr] = arr[index_num] 
        index_arr += (2 - int(index_arr >= 2 * min_portion - 1))
        index_num += 1

    return new_array    




def rearrange_simpler(arr):
    n = len(arr)
    n_pos = 0
    n_neg = 0

    for v in arr:
        n_pos += int(v >= 0)
        n_neg += int(v < 0)

    pos_num = [0 for _ in range(n_pos)]
    neg_num = [0 for _ in range(n_neg)]

    p1, p2 = 0, 0

    for v in arr:

        if v >= 0:
            pos_num[p1] = v
            p1 += 1
        else:
            neg_num[p2] = v
            p2 += 1


    new_array = [0 for _ in range(n)]

    p1, p2 = 0, 0
    counter = 0

    while counter < n: 
        
        if p1 < n_pos:
            new_array[counter] = pos_num[p1]
            counter += 1   
            p1 += 1

        if p2 < n_neg:
            new_array[counter] = neg_num[p2]
            counter += 1
            p2 += 1

    return new_array