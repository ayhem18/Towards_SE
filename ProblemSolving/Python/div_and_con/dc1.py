from typing import List

def __binary_search(a: List[int], x: int, low: int, high: int):
    if low > high:
        return -1

    mid = (low + high) // 2

    if a[mid] == x:
        return mid

    if a[mid] < x:
        return __binary_search(a, x, mid + 1, high)

    return __binary_search(a, x, low, mid - 1)


def search(a: List[int], x: int) -> int:
    return __binary_search(a, x, 0, len(a) - 1)



"""
https://leetcode.com/problems/search-a-2d-matrix/
"""
def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    # let's rule some basic cases
    if target < matrix[0][0]:
        return False
    
    if target >= matrix[-1][0]:
        index = search(matrix[-1], target)
        return index != -1
    
    # we will keep the invaraniant m[high][0] > target >= m[low][0]

    low, high = 0, len(matrix) - 1
    
    while high - low > 1:
        mid = (high + low) // 2
        if matrix[mid][0] <= target:
            low = mid
        else:
            high = mid
    
    # at this point we know that high = low + 1
    index = search(a=matrix[low],x=target)
    return index != -1


"""
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/
"""

def findMin(nums: List[int]) -> int:
    n = len(nums)
    l, h = 0, n - 1
    while l < h and nums[l] > nums[h]:
        mid = (l + h) // 2

        if nums[mid] > nums[h]:
            l = mid + 1

        elif nums[l] > nums[mid]:
            l += 1
            h = mid

    return nums[l]            

