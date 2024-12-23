"""
The idea of 2 pointers might have been tightly associated to some specific set of problems, but the idea is quite general.
"""

from typing import List, Optional


# https://www.geeksforgeeks.org/problems/two-numbers-with-sum-closest-to-zero1737/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

def closestToZero (arr: List[int], n: Optional[int] = None) -> int:
    """
    This function finds the pair with the sum closest to zero. Such a sum is equivalent to find the sum with the minimum absolute value. 
    """    

    # sort the array as it is not necessarily sorted
    arr = sorted(arr)

    # set the length of the array
    n = len(arr) if n is None else n

    # set the pointers
    p1, p2 = 0, n - 1

    best_sum = arr[p1] + arr[p2]
    current_sum = best_sum

    while p1 < p2:
        # the idea is simple
        current_sum = arr[p1] + arr[p2] 

        best_sum = min([current_sum, best_sum], key=lambda x: (abs(x), -x))
        
        if current_sum > 0:
            p2 -= 1

        elif current_sum < 0:            
            p1 += 1
        
        else:
            return 0
        

    return best_sum
