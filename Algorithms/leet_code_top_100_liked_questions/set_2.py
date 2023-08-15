"""
The 1st script reached around 600 lines. Time for a 2nd script
"""

from typing import List


# noinspection PyMethodMayBeStatic,PyShadowingNames
class Solution:
    # starting with an easy one:
    # https://leetcode.com/problems/search-insert-position/
    def search_index(self, nums: List[int], target: int, low: int, high: int):
        # let's start with the particular case of one-element
        if len(nums) == 1:
            return 1 if target > nums[0] else 0

        if target > nums[high]:
            return high + 1
        if target < nums[low]:
            return low

        mid = (low + high) // 2

        if nums[mid] == target:
            return mid

        if nums[mid] > target > nums[mid - 1]:
            return mid
        if nums[mid + 1] > target > nums[mid]:
            return mid + 1

        if nums[mid] > target:
            return self.search_index(nums, target, low, mid - 1)

        return self.search_index(nums, target, mid + 1, high)

    def searchInsert(self, nums: List[int], target: int) -> int:
        return self.search_index(nums, target, 0, len(nums) - 1)


if __name__ == '__main__':
    sol = Solution()
    a = [1, 3, 5, 6, 10]

    for i in range(a[0], a[-1] + 5):
        print(f"number: {i}")
        print(f"index: {sol.searchInsert(a, i)}")
        print("#" * 10)

