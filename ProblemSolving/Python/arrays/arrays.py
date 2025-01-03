"""
This file contains my solutions for some problems on 'arrays'
"""


    
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
