"""
The 1st script reached around 600 lines. Time for a 2nd script
"""

from typing import List
from heapq import heapify, heappush, heappop
from collections import OrderedDict, Counter
from math import ceil


# noinspection PyMethodMayBeStatic,PyShadowingNames,PyPep8Naming
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

    # let's define a special tuple for our problem here
    class SlideTuple:
        def __init__(self, index: int, value: int, k: int):
            self.index = index
            self.value = value
            self.k = k

        def __lt__(self, nxt):
            return self.value < nxt.yos

    class SlideTuple:
        def __init__(self, index: int, val: int):
            self.index = index
            self.val = val

        def __lt__(self, other):
            return self.val < other.val or self.val == other.val and self.index < other.index

        def __eq__(self, other):
            return self.val == other.val and self.index == other.index

        def __gt__(self, other):
            return self.val > other.val or (self.val == other.val and self.index > other.index)

        def __getitem__(self, item):
            return self.index if item == 0 else self.val

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:

        heap = [self.SlideTuple(index, -v) for index, v in enumerate(nums[:k])]
        heapify(heap)
        save = OrderedDict()

        def find_max_element(i):
            while True:
                index, val = heap[0][0], -heap[0][1]
                if i + k - 1 >= index >= i:
                    return index, val
                else:
                    # remove the element
                    heappop(heap)

        for i in range(0, len(nums) - k):
            # find the maximum element
            max_index, max_element = find_max_element(i)
            save[i] = max_element
            # only pop the element if it is the maximum number
            if max_index == i and max_element == nums[i]:
                heappop(heap)
            heappush(heap, self.SlideTuple(i + k, -nums[i + k]))

        save[len(nums) - k] = find_max_element(len(nums) - k)[1]
        return [v for k, v in save.items()]

    # a problem listed as medium for some reason...
    # well it is definitely annoying...
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        C, R = len(matrix[0]), len(matrix)
        if C == 1:
            return [row[0] for row in matrix]

        if R == 1:
            return matrix[0]

        lower_row, upper_row = 0, R - 1
        lower_col, upper_col = 0, C - 1
        res = []
        count = 0

        while lower_row <= upper_row and lower_col <= upper_col:
            if count < R * C:
                for i in range(lower_col, upper_col + 1):
                    res.append(matrix[lower_row][i])
                    count += 1

            lower_row += 1
            if count < R * C:
                for j in range(lower_row, upper_row + 1):
                    res.append(matrix[j][upper_col])
                    count += 1

            upper_col -= 1
            if count < R * C:
                for i in range(upper_col, lower_col - 1, -1):
                    res.append(matrix[upper_row][i])
                    count += 1

            upper_row -= 1
            if count < R * C:
                for j in range(upper_row, lower_row - 1, -1):
                    res.append(matrix[j][lower_col])
                    count += 1

            lower_col += 1

        return res

    def lengthOfLIS(self, nums: List[int]) -> int:
        # my solution is DP, and quadratic in time
        # apparently there is a O(nlog(n)) solution
        # but let's make this work for the moment
        values = [0 for _ in nums]

        if len(nums) == 1:
            return 1

        values[1] = 1 + int(nums[-2] < nums[-1])
        max_value = values[1]
        for i in range(len(nums) - 3, -1, -1):
            # each iteration will set values[len(nums) - 1 - i] which corresponds to length of LTS
            # starting from i
            j1 = None
            for j in range(i + 1, len(nums)):
                if nums[j] > nums[i]:
                    j1 = j
                    break

            if j1 is None:
                values[len(nums) - 1 - i] = 1
                continue
            candidates = [j1]
            candidates.extend([c for c in range(j1, len(nums)) if nums[j1] > nums[c] > nums[i]])

            values[len(nums) - 1 - i] = 1 + max([values[len(nums) - 1 - c] for c in candidates])

            max_value = max(max_value, values[len(nums) - 1 - i])

        return max_value

    # what about the follow-up question ? O(nlog(n))
    def reorganizeString(self, s: str) -> str:
        # the idea is quite simple here
        counter = sorted(list(Counter(s)), key=lambda x: x[1], reverse=True)
        new_string = ["" for _ in s]

        if counter[0][1] > int(ceil(len(s) / 2)):
            return ""

        i = 0

        # that's the occupying stage
        letter = 0
        while True:
            for _ in range(counter[letter][1]):
                new_string[i] = counter[letter][0]
                i += 2
                if i > len(s):
                    break
            letter += 1




if __name__ == '__main__':
    sol = Solution()
    a = [10, 9, 2, 5, 3, 7, 101, 18]
    print(sol.lengthOfLIS(a))
