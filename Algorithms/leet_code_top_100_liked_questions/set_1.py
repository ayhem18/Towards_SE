"""
This script contains my solutions for some of the problems I haven't previously solved in the
top 100 liked questions in LeetCode.
"""
from collections import deque
from typing import List


# let's start with the following problem:
# https://leetcode.com/problems/swap-nodes-in-pairs/
# well I wrote it in the linkedlist file for completion


# noinspection PyMethodMayBeStatic,PyShadowingNames
class Solution:
    # well I overcame my fear and decided to tackle a 'hard' problem.
    # https://leetcode.com/problems/longest-valid-parentheses/
    # of course it won't be solved in a single function
    OPEN = '('
    CLOSE = ')'

    # so this solution fails at the last test...
    def first_index_valid(self, string: str, start_index: int) -> int:
        # this function will return the first index 'i' for which string[start_index :i + 1] is with valid parentheses
        # and -1 in case there is no such substring

        stack = deque()
        for index, char in enumerate(string[start_index:], start_index):
            if char == self.OPEN:
                stack.append(char)
            else:
                # the stack is either empty of not
                if len(stack) == 0:
                    # to reach this part of the code, it just means start_index is a closed character
                    return -index

                stack.pop()
                # now check if the stack is empty
                if len(stack) == 0:
                    # we just found our 'index'
                    return index

        # if the code reaches this point, the stack is not empty and thus there is not such substring
        return - (start_index + len(stack) - 1)

    def building_substrings(self, string: str) -> list[tuple[int, int]]:
        index = 0
        building_blocks = []
        while index < len(string):
            next_index = self.first_index_valid(string, index)
            if next_index > 0:
                # add the pair of indices
                building_blocks.append((index, next_index))
                index = next_index
            # if no well-formed substrings starting from index were found, simply increment 'index'
            else:
                index = -next_index
            index += 1
        return building_blocks

    def longest_valid_substring(self, string: str, pairs: list[tuple[int, int]]):
        if len(pairs) == 0:
            return 0

        start, end = pairs[0]
        largest_str = ""
        largest_length = 0
        for v1, v2 in pairs:
            if v1 > end + 1:
                # evaluate
                largest_str = max(string[start:end + 1], largest_str, key=len)
                largest_length = max(largest_length, end - start + 1)
                # set the new values
                start = v1
            end = v2

        # in case the largest block is actually at the end
        largest_str = max(string[start:end + 1], largest_str, key=len)
        largest_length = max(largest_length, end - start + 1)

        return largest_length

    def longestValidParentheses(self, string: str) -> int:
        if len(string) <= 1:
            return 0
        # first find the pairs
        pairs = self.building_substrings(string)
        res = self.longest_valid_substring(string, pairs)
        return res

    ##############################################################################################
    ##############################################################################################
    ##############################################################################################

    # well I need to do something a bit easier now: a medium problem ?
    # https://leetcode.com/problems/maximum-subarray/
    def maxSubArrayIndices(self, nums: List[int]) -> tuple[int, int]:
        # let's set our variables
        start, end = 0, 0
        current_sum = 0
        best_sum = float('-inf')  # minus infinity
        best_start, best_end = 0, 0
        while end < len(nums):
            current_sum += nums[end]
            if current_sum > best_sum:
                best_sum = current_sum
                best_start = start
                best_end = end
            if current_sum < 0:
                start = end + 1
                # the sum should start from zero
                current_sum = 0
            end += 1

        if current_sum > best_sum >= 0:
            best_sum = current_sum
            best_start = start
            best_end = end

        return best_start, best_end

    def maxSubArray(self, nums: List[int]) -> int:
        best_start, best_end = self.maxSubArrayIndices(nums)
        # print(nums[best_start: best_end + 1])
        return sum(nums[best_start: best_end + 1])

    # nice !! time to move on!!
    # well rotating an array in place shouldn't be too hard
    # it is a wonder why this problem is classified as 'medium'

    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # first let's convert 'k' to its value mod (n)
        k = k % len(nums)
        last_k = nums[-k:]
        for i in range(len(nums) - k - 1, -1, -1):
            nums[i + k] = nums[i]
        for i in range(k):
            nums[i] = last_k[i]

    # word break problem broke me a bit
    # https://leetcode.com/problems/word-break/
    # my attempt keeps getting LTE flag which is quite sad...
    def InnerWordBreak(self, string: str, wordDict: List[str], memo: dict[str, bool] = None) -> bool:
        if memo is None:
            memo = {}

        # let's start with some base cases
        if len(string) == 0:
            return True
        # let's rule out some edges cases

        if string in memo:
            return memo[string]

        # sorted by the largest word
        possible_words_starts = sorted([w for w in wordDict if string.startswith(w)], key=len, reverse=True)

        if len(possible_words_starts) == 0:
            return False

        for w in possible_words_starts:
            if w == string:
                return True
            # do not forget to pass the memo object
            temp = self.InnerWordBreak(string[len(w):], wordDict, memo)
            if temp:
                return True

        return False

    def wordBreak(self, string: str, wordDict: List[str]) -> bool:
        # the set of letters present in the string is a subset
        # of the set of all characters in the wordDict list
        word_dict_set = set()
        string_set = set(string)

        for w in wordDict:
            word_dict_set = word_dict_set.union(set(w))

        if not string_set.issubset(word_dict_set):
            return False

        # it might be necessary to filter the word dict to only keep

        return self.InnerWordBreak(string, wordDict)

    # this problem is interesting as well
    # https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

    # one simple approach is to get each of the 2 extremes separately

    # well that's one great solution, NGL
    def higher_occurrence(self, nums: list[int], target: int, low: int, high: int):
        # let's start with the classical base cases
        if high < low:
            return -1

        if nums[high] == target:
            return high

        # time to consider mid
        mid = (low + high) // 2

        if nums[mid] < target:
            # mid + 1, high - 1 (high does not equal target so no point in checking it)
            return self.higher_occurrence(nums, target, mid + 1, high - 1)

        if nums[mid] == target:
            # we know that the higher occurrence of target is at least 'mid', let's consider mid and above
            return self.higher_occurrence(nums, target, mid, high - 1)

        # now target < nums[mid]
        return self.higher_occurrence(nums, target, low, mid - 1)

    def lower_occurrence(self, nums: list[int], target: int, low: int, high: int):
        # let's start with the classical base cases
        if high < low:
            return -1

        if nums[low] == target:
            return low

        # time to consider mid
        mid = (low + high) // 2

        if nums[mid] < target:
            # mid + 1, high - 1 (high does not equal target so no point in checking it)
            return self.lower_occurrence(nums, target, mid + 1, high)

        if nums[mid] == target:
            # we know that the lower occurrence is at most 'mid', let's check mid and lower
            # we know that the higher occurrence of target is at least 'mid', let's consider mid and above
            return self.lower_occurrence(nums, target, low + 1, mid)

        # now target < nums[mid]
        return self.lower_occurrence(nums, target, low + 1, mid - 1)

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # the time complexity must be O(log(n))
        e1, e2 = self.lower_occurrence(nums, target, 0, len(nums) - 1), \
            self.higher_occurrence(nums, target, 0, len(nums) - 1)
        return [e1, e2]

    def minPathSumRecur(self, grid: List[List[int]], y: int, x: int, memo: dict[tuple, int] = None) -> int:
        if memo is None:
            memo = {}

        # the idea here is simple
        if y == len(grid) - 1 and x == len(grid[0]) - 1:
            return grid[y][x]

        key = (y, x)
        if key in memo:
            return memo[key]

        cost_right = self.minPathSumRecur(grid, y, x + 1, memo) if x + 1 < len(grid[0]) else float('inf')
        cost_down = self.minPathSumRecur(grid, y + 1, x, memo) if y + 1 < len(grid) else float('inf')

        memo[key] = grid[y][x] + min(cost_right, cost_down)
        return memo[key]

    def minPathSum(self, grid: List[List[int]]) -> int:
        return self.minPathSumRecur(grid, 0, 0)


if __name__ == "__main__":
    sol = Solution()
    # nums = [1, 2, 2, 2, 2, 3, 5, 10, 10, 10, 12, 12, 50]
    nums = [1] * 10
    print(sol.searchRange(nums, 1))
