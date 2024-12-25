"""
This script contains my solutions for array problems on gfg
"""

from typing import List
from collections import deque


# https://www.geeksforgeeks.org/problems/sorted-subsequence-of-size-3/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
# one of the most difficult problems I have tried to solve


# I need to create a special data structure
class threeMaxStack:
    def __init__(self):
        self.s = deque()
    
    def add(self, val: int) -> int:
        
        if len(self.s) == 0:
            self.s.append(val)
            return 0

        if len(self.s) == 1:
            # if the new value is less or equal to the current value
            # then simply substitute it
            if val <= self.s[0]:
                self.s[0] = val
                return 0
            
            # at this point we have only one value at the queue and 
            # the new value is larger than the current value, so add it
            self.s.append(val)
            return 0

        # at this point: len(self.s) == 2
        if val > self.s[-1]:
            # this means we have 3 sorted elements
            self.s.append(val)
            return 1 

        # the new element is less or equal to the last element
        if self.s[0] < val <= self.s[-1]:
            self.s[-1] = val
            return 0

        # this means that val is less than the very first element: "val" should be moved to the second stack !!!    
        return -1
    
    def clear(self):
        self.s.clear()

    def copy(self, another: 'threeMaxStack'):
        self.s = another.s.copy()


    def __len__(self) -> int:
        return len(self.s)


def find3Numbers(arr: List[int]) -> List[int]:
    if len(arr) < 3:
        return False
    
    if len(arr) == 3:
        return arr[0] < arr[1] and arr[1] < arr[2]
    
    s1 = threeMaxStack()
    s2 = threeMaxStack()

    for v in arr:
        a1 = s1.add(v)
        
        if a1 == 1:
            return True
        
        if a1 == -1:
            s2.add(v)
            
            if len(s2) == 2:
                s1.copy(s2)
                s2.clear()
            
    return False

