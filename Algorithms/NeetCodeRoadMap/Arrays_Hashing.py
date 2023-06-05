"""
In this script I solve the Arrays&Hashing problems from the NeetCode LeetCode roadmap:
"""

from collections import Counter
import numpy as np
from heapq import heapify, heappush, heappop


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        # first sort the values
        nums_sorted = sorted(nums)
        for i in range(1, len(nums_sorted)):
            if nums_sorted[i] == nums_sorted[i - 1]:
                return True

        return False

    # better solution ?
    # def containsDuplicate(self, nums: list[int]) -> bool:
    #     return len(nums) != len(set(nums))

    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)

    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)

    # binary search
    def binary_search(self, array: list, x, low, high):
        while low <= high:

            mid = low + (high - low) // 2

            if array[mid] == x:
                return mid

            elif array[mid] < x:
                low = mid + 1

            else:
                high = mid - 1

        return -1

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # first sort the array of values
        sorted_nums = sorted(nums)
        length = len(nums)
        res = []
        for n in nums:
            # this means the pair was found
            if self.binary_search(sorted_nums, target - n, low=0, high=length - 1) != -1:
                for i in range(len(nums)):
                    if nums[i] == n and len(res) == 0:
                        res.append(i)
                    elif nums[i] == target - n and i not in res:
                        res.append(i)
                        return res
                res.clear()

        return [-1, -1]

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # the idea here is to find the indices of 2 distinct elements
        # that sum up to target
        # the best solution so far performance-wise
        m = {}

        for index, val in enumerate(nums):
            m[target - val] = index

        for index, val in enumerate(nums):
            if val in m and index != m[val]:
                return [index, m[val]]

        return [-1, -1]

    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        strs_copy = np.asarray(strs)
        m = {}
        # first, let's start with mapping each string in the list to its sorted version
        for index, s in enumerate(strs):
            ss = "".join(sorted(s))
            if ss not in m:
                m[ss] = []
            m[ss].append(index)

        return [list(strs_copy[indices]) for _, indices in m.items()]

    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        # first create a heap for top k frequencies
        k_heap = []
        heapify(k_heap)
        counter = Counter(nums)
        for n, freq in counter.items():
            if len(k_heap) < k:
                heappush(k_heap, (freq, n))
            else:
                # now there k elements in the heap
                # we need to check whether to remove one of them
                min_freq = k_heap[0][0]

                if min_freq < freq:
                    heappop(k_heap)
                    heappush(k_heap, (freq, n))

        return [k_heap[i][1] for i in range(len(k_heap))]

    # apparently I misunderstood the task, well, this is not a bad problem to solve either way

    # def longestConsecutive(self, nums: list[int]) -> int:
    #     m = {}
    #     # if the list is empty return 0
    #     if len(nums) == 0:
    #         return 0
    #
    #     max_length = 1
    #     for value in nums[1:]:
    #         if value - 1 in m:
    #             new_length = m[value - 1] + 1
    #             m[value] = new_length
    #             max_length = max(max_length, new_length)
    #             del(m[value - 1])
    #         else:
    #             m[value] = 1
    #
    #     return max_length

    def longestConsecutive(self, nums: list[int]) -> int:
        # first let's convert the list to a set
        set_nums = set(nums)
        max_count = 0
        while len(set_nums) > 0:
            for v in nums:
                # save ourselves some time
                if v not in set_nums:
                    continue

                # define the number of consecutive elements less than v
                c_minus = 1
                c_plus = 1
                # count the consecutive numbers larger than v
                while v + c_plus in set_nums:
                    set_nums.remove(v + c_plus)
                    c_plus += 1

                # count the consecutive numbers smaller than v
                while v - c_minus in set_nums:
                    set_nums.remove(v - c_minus)
                    c_minus += 1

                # remove v
                set_nums.remove(v)
                new_count = (v + c_plus) - (v - c_minus) - 1
                max_count = max(new_count, max_count)

        return max_count


if __name__ == '__main__':
    s = Solution()
    nums = [1, 2, 3, 8, 9, 10, 12, 13, 14, 15]
    nums = [1]
    print(s.longestConsecutive(nums))
