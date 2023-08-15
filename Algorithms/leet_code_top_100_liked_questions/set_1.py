"""
This script contains my solutions for some of the problems I haven't previously solved in the
top 100 liked questions in LeetCode.
"""
import math
from collections import deque, Counter
from typing import List, Optional
from heapq import heapify


# let's start with the following problem:
# https://leetcode.com/problems/swap-nodes-in-pairs/
# well I wrote it in the linkedlist file for completion


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next = next_node


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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

    # another obvious DP problem: nothing too challenging
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

    # let's solve this problem:
    # https://leetcode.com/problems/subarray-sum-equals-k/
    def subarraySum(self, nums: List[int], k: int) -> int:
        # the simplest solution is too slow
        # let's write some more sophisticated algorithm
        if len(nums) == 1:
            return int(nums[0] == k)

        n = len(nums)
        # let's introduce the idea of range or a block: consecutive array elements of the same sign

        # we need a mapping between any index and the block it belongs to
        index_to_range = {}

        current_start = 0
        current_end = 0

        for index, value in enumerate(nums[1:], 1):
            if (value >= 0 and nums[current_start] >= 0) or (value < 0 and nums[current_start] < 0):
                current_end = index
            else:
                index_to_range[current_start] = (current_start, current_end)
                current_start = index
                current_end = index

        index_to_range[current_start] = (current_start, current_end)

        index_to_sums = {}
        for start, (s, e) in index_to_range.items():
            # 'start' should be equal to 's'
            current_sum = 0
            for i in range(e, s - 1, -1):
                current_sum += nums[i]
                index_to_sums[i] = current_sum

        initial_items = list(index_to_range.items())
        for start, (s, e) in initial_items:
            for i in range(s, e + 1):
                index_to_range[i] = (s, e)

        count = 0
        for i in range(n):
            current_sum = nums[i]
            index = i
            while index < n:
                start, end = index_to_range[index]
                block_sum_index = index_to_sums[index]

                if current_sum < k:
                    current_sum = 0 if index == i else current_sum

                    if current_sum + block_sum_index == k:
                        # increase the count
                        count += 1
                    elif current_sum + block_sum_index > k:
                        ts = current_sum
                        for j in range(index, end + 1):
                            ts += nums[j]
                            if ts == k:
                                count += 1
                                break

                elif current_sum > k:
                    current_sum = 0 if index == i else current_sum

                    if current_sum + block_sum_index == k:
                        # increase the count
                        count += 1
                    elif current_sum + block_sum_index < k:
                        ts = current_sum
                        for j in range(index, end + 1):
                            ts += nums[j]
                            if ts == k:
                                count += 1
                                break
                    # anyway, the sum of the block is added
                    # and the index if moved to the start of the next block

                else:
                    if index == i:
                        j = index + 1
                        while j < n and nums[j] == 0:
                            count += 1
                            j += 1
                    else:
                        # start from index
                        j = index
                        while j < n and nums[j] == 0:
                            count += 1
                            j += 1

                index = end + 1
                current_sum += block_sum_index

        return count

    def subarraySumSlow(self, nums: List[int], k: int) -> int:
        n = len(nums)
        count = 0
        for i in range(n):
            current_sum = 0

            for number in nums[i:]:
                current_sum += number
                count += int(current_sum == k)

            # current_sum at this point is the sum of the entire slice
            # slice_sum = current_sum
            # current_sum = 0
            # for number in nums[i:]:
            #     current_sum += number
            #     count += int(current_sum == slice_sum - k)

        return count

    # word break problem broke me a bit
    # https://leetcode.com/problems/word-break/
    # my attempt keeps getting LTE flag which is quite sad...
    def innerWordBreak(self,
                       string: str,
                       char_count: Counter[str, int],
                       char_word_map: dict[str, set[str]],
                       memo: dict[str, bool] = None):

        memo = {} if memo is None else memo
        # let's put the trivial case aside
        if len(string) == 0:
            return True

        if string in memo:
            return memo[string]

        # map the characters to their total number of occurrences
        string_char_count = Counter(string)
        # find the char that has minimal occurrence in the string
        # equality is broken by the number of words for which the character belongs to in the
        # wordDict
        min_char = string[0]
        for c in string:
            min_char = min([c, min_char], key=lambda x: (string_char_count[x], len(char_word_map[x])))

        # find the indices of min_char in the string
        indices = [i for i, c in enumerate(string) if c == min_char]

        # choose the indices that divide the original string to the most balanced substrings (length wise)
        key_index = min(indices, key=lambda x: abs(len(string) / 2 - x))

        candidates = char_word_map[min_char]

        for cs in candidates:

            if cs == string:
                memo[string] = True
                return True

            for index, char in enumerate(cs):
                if char == min_char:
                    right_length = key_index >= index
                    left_length = len(string) - key_index >= len(cs) - index
                    match = string[key_index - index: key_index - index + len(cs)] == cs
                    if right_length and left_length and match:
                        # time to solve the sub-problems
                        # the right side
                        temp = self.innerWordBreak(string[:key_index - index],
                                                   char_count,
                                                   char_word_map,
                                                   memo) and self.innerWordBreak(string[key_index - index + len(cs):],
                                                                                 char_count,
                                                                                 char_word_map,
                                                                                 memo)
                        if temp:
                            memo[string] = True
                            return True

        # save the result in the memo
        memo[string] = False
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

        # let's prepare some more information needed for a constant time look up
        char_count = Counter()
        char_word_map = {}
        # we need to have the total number of occurrences of each char in the word bank
        for word in wordDict:
            for c in word:
                if c not in char_word_map:
                    char_word_map[c] = set()
                char_word_map[c].add(word)
            char_count.update(word)

        # char_Count: maps each character to the total number of occurrences in the word bank
        # char_word_map: maps each character to all words that contains the char in question

        return self.innerWordBreak(string, char_count, char_word_map)

    # this problem sounds interesting:
    # https://leetcode.com/problems/set-matrix-zeroes/
    # apparently my solution is quite good: beats 90% performance wise and 84% memory-wise
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # this problem mainly deals with optimizing memory usage
        columns = set()

        for r in range(len(matrix)):
            zero_row = False

            for c in range(len(matrix[0])):
                if matrix[r][c] == 0:
                    # first add `c` to the cols to consider
                    columns.add(c)
                    # set the zero_row to `True`
                    zero_row = True
                    # set the value [y][c] to zero where y < r
                    for t in range(r):
                        matrix[t][c] = 0

            if zero_row:
                for i in range(len(matrix[0])):
                    matrix[r][i] = 0
            else:
                for i in range(len(matrix[0])):
                    if i in columns:
                        matrix[r][i] = 0

    # it sounds easier than it is
    # the heaps acts very strangely with negative numbers
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # first creates a counter here
        # heap = list(set([-v for v in nums]))
        heap = list(set(nums))
        heapify(heap)
        count = 0
        # create a counter
        counter = Counter(nums)
        current_num = heap.pop()

        while True:
            if count + counter[current_num] >= k:
                return current_num
            count += counter[current_num]
            current_num = heap.pop()

    # here is this one: https://leetcode.com/problems/partition-list/
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        if head is None:
            return head
        t = head
        new_head = None
        last_node = None
        while t is not None:
            if t.val < x:
                if new_head is None:
                    new_head = ListNode(t.val)
                    last_node = new_head
                else:
                    last_node.next = ListNode(t.val)
                    last_node = last_node.next

        # this is the case where there are no number that are less than x
        if last_node is None:
            return head

        t = head
        while t is not None:
            if t.val >= x:
                last_node.next = ListNode(t.val)
                last_node = last_node.next
        return new_head

    # this question has 46% success rate
    # https://leetcode.com/problems/merge-intervals/description/
    # well done, no problem:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # first let's sort the intervals
        intervals = sorted(intervals, key=lambda e: (e[0], -e[1]))
        start, end = None, None
        result = []
        for i in intervals:
            if start is None:
                start = i[0]
                end = i[1]
                continue
            if i[0] > end:
                result.append([start, end])
                start, end = i
            else:
                end = max(end, i[1])
        # add the last interval
        result.append([start, end])
        return result


if __name__ == "__main__":
    sol = Solution()
    ins = [[2, 3], [3, 4], [4, 5], [5, 7], [1, 2]]
    # ins = [[1,3],[2,6],[8,10],[15,18]]
    print(sol.merge(ins))
