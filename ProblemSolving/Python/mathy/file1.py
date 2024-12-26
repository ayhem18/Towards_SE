"""
This script contains my solutions to problem that can be solved (or maybe optimized) based on math tricks
"""

from typing import List
from math_utils import greatest_common_divisor


# this problem is the reason, I am considering studying Number Theory once again
# rotate an array with any K using O(1) space

# the main trick is to know which numbers represent a cylce: 
# if n ^ k = 1, no elements will collide
# otherwise, consider the gcd = n ^ k = 1
# and numbers of the same reminder with respect to gcd will represent a cycle: in other words
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


# https://www.geeksforgeeks.org/problems/sum-of-subarrays2229/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
# the problem find the total sum of all sub arrays in a given array

# the main idea is very similar to swapping two sums: instead of focusing on the sum of each sub array: determine the number of sums each element
# is included in and simply multiply that number of the element (and then sum all of these individual numbers)

def subarraySum(arr: List[int]):
    M = 10 ** 9 + 7
    s = 0
    n = len(arr)

    for index, v in enumerate(arr):
        occ = ((index + 1) * (n - index)) % M
        s += ((v * occ) % M)
        s = s % M
    
    return s


# https://www.geeksforgeeks.org/problems/find-repetitive-element-from-1-to-n-1/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

# the idea is to know the sum of 1 + 2 + ... n (to solve it in o(1) of course)
def findDuplicate(arr: List[int]):
    pass


def missingNumber(arr: List[int]):
    s = sum(arr)
    n = len(arr)
    total = ((n + 1) * (n + 2)) // 2
    return total - s
