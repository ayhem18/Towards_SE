"""
This script contains the implementation of standard backtracking problems such as: 

1. all subsets of size k
2. all subsets of a given set
3. all permutations of a sequence (array / string)
"""

from typing import List

def choose_k_from_set(nums: list[int], k: int):
    if k > len(nums) or k == 0:
        return [[]]

    if k == 1:
        return [[n] for n in nums]

    if k == len(nums):
        return [nums]
    

    res = []

    # either choose the first eleme nt and then add all subsets of size (k - 1)
    # or ignore the first element and take all "k" elements from nums[1:]
    temp = choose_k_from_set(nums[1:], k - 1)
    for i in range(len(temp)):
        temp[i] = [nums[0]] + temp[i]
    res.extend(temp)

    if len(nums) >= k + 1:
        temp = choose_k_from_set(nums[1:], k)
        res.extend(temp)

    return res


def all_bit_masks(n: int) -> List[int]:
    """Given a certain length "n", generate all possible bit masks

    Args:
        n (int): length of the bit mask

    Returns:
        List[int]: a list of binary lists
    """

    if n < 1:
        return []
    
    if n == 1:
        return [[0], [1]]
    
    base_binary_masks = all_bit_masks(n - 1)
    
    res = [[0] + bm for bm in base_binary_masks] + [[1] + bm for bm in base_binary_masks]

    return res


def select_elements_by_binary_mask(array: List[int], binary_mask: List[int]) -> List[int]:
    """
    Args:
        array (List[int])
        binary_mask (List[int]): an array with binary values binary_mask[i] determines whether the i-th element in the "array" should be selected or not

    Returns:
        List[int]: the array with the selected elements
    """
    length = sum(binary_mask)
    filtered_array = [0 for _ in range(length)]
    counter = 0
    for index, bit in enumerate(binary_mask):
        if bit == 1:
            filtered_array[counter] = array[index]
            counter += 1
    
    return filtered_array
    
def all_subsets(array: List[int]) -> List[List[int]]:
    # a subset can be seen as a bit mask applied on the array
    # finding all subsets is equivalent to finding all bit masks of the size of the array

    masks = all_bit_masks(len(array))
    return [select_elements_by_binary_mask(array, m) for m in masks]



