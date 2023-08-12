"""
This file contains my solutions for the leet code problems proposed in the 1d DP problems:
https://neetcode.io/roadmap
"""
import math
from typing import List
import numpy as np
from collections import Counter


# noinspection PyMethodMayBeStatic,PyShadowingNames
class Solution:
    # https://leetcode.com/problems/climbing-stairs/
    def climbStairs(self, n: int, memo=None) -> int:
        # let's do it with memo
        if memo is None:
            memo = {}
        # the idea here is simple
        if n < 0:
            return 0
        if n == 0:
            return 1

        if n in memo:
            return memo[n]

        memo[n] = self.climbStairs(n - 1, memo) + self.climbStairs(n - 2, memo)
        return memo[n]

    def cost_function(self, cs: List[int], n: int, memo: dict = None):
        if memo is None:
            memo = {}

        if n < 0:
            return 0

        if n in memo:
            return memo[n]

        cn = cs[n] + min(self.cost_function(cs, n - 1, memo), self.cost_function(cs, n - 2, memo))
        memo[n] = cn
        return cn

    def minCostClimbingStairs(self, cs: List[int], memo: dict = None) -> int:
        n = len(cs)
        cs.append(0)
        return self.cost_function(cs, n, memo)

    # let's move on to more serious challenges
    # https://leetcode.com/problems/house-robber/

    def inner_rob(self, nums: list[int], n: int, memo: dict = None):
        if memo is None:
            memo = {}
        # let's start with some base cases
        if n < 0:
            return 0

        if n == 0:
            return nums[0]
        if n == 1:
            return max(nums[0], nums[1])

        # now n >= 3: the length of the array is at least 3
        if n in memo:
            return memo[n]

        # there are 2 options
        # either steal from house n - 1, then we cannot steal from house n - 2
        # or start stealing from house n - 2 directly
        memo[n] = max(self.inner_rob(nums, n - 1, memo),
                      nums[n] + self.inner_rob(nums, n - 2, memo))
        return memo[n]

    # def rob(self, nums: List[int]) -> int:
    #     return self.inner_rob(nums, len(nums) - 1)

    # seems robbers have another version
    def rob(self, nums: List[int]) -> int:
        # there are 2 possibilities, either using the last element or not
        # if we use the last element: then we cannot use the first one, and the second last one
        p1 = nums[-1]
        new_nums = nums[1:-2]
        p1 += self.inner_rob(new_nums, len(new_nums) - 1)
        # the 2nd option is not to use the last element
        p2 = self.inner_rob(nums[:-1], len(nums) - 2)
        return max(p1, p2)

    # time for a slightly more challenging string problem:
    # longest palindromic substring
    # let's break down a notch
    # the brute force approach works in O(n^3)
    # let's bring down  to O(n ^ 2)
    def longest_palindrome_start(self, string: str) -> str:
        """
        This function finds the longest palindrome that starts from the beginning of the string in linear time
        """
        if len(string) == 1:
            return string[0]

        if len(string) == 2:
            return string if string[0] == string[1] else string[0]

        # at this point of the code len(string) >= 3

        best_str = string[:2] if string[0] == string[1] else string[0]  # one letter string is a palindrome...
        p1, p2 = 0, 1
        last_len_pal = 1 if string[0] == string[1] else 0
        set_chars = set(string[:2])

        for i, char in enumerate(string[2:], start=2):
            if i % 2 == 0:
                p2 += 1

            if i % 2 == 1:
                p1 += 1

            set_chars.add(char)
            if last_len_pal == i - 1:
                # this means the last detected palindrome was the previous substring
                # then this new substring is a palindrome only and only if all characters so far are the same
                if len(set_chars) == 1:
                    last_len_pal += 1
                    best_str = string[: i + 1]

                # no need to proceed to the next part
                continue
            tp1, tp2 = p1, p2
            # time to evaluate w
            while tp1 > -1 and tp2 <= i and string[tp1] == string[tp2]:
                tp1 -= 1
                tp2 += 1

            # at this point there 2 cases:
            # either p1 == -1 and p2 == len(string) which means the string is palindrome
            if tp1 == -1 and tp2 == i + 1:
                last_len_pal = i
                best_str = string[: i + 1]

        return best_str

    def longestPalindrome(self, s: str) -> str:
        if len(s) <= 2:
            return self.longest_palindrome_start(s)

        current_best = ""
        for i in range(len(s)):
            # this means the length of the substring left is less than the current best, so there is no point
            # in considering it
            if len(s) - i < len(current_best):
                break

            temp = self.longest_palindrome_start(s[i:])
            current_best = max(temp, current_best, key=len)

        return current_best

    def all_palindromes_start(self, string: str) -> set[str]:
        """
            This function returns all palindrome substring that start from the beginning of the string.
        """
        if len(string) == 1:
            return {string}

        pals = set([string[0], string[:2]] if string[0] == string[1] else [string[0]])
        if len(string) == 2:
            return set(pals)

        # at this point of the code len(string) >= 3
        p1, p2 = 0, 1
        last_len_pal = 1 if string[0] == string[1] else 0
        set_chars = set(string[:2])

        for i, char in enumerate(string[2:], start=2):
            if i % 2 == 0:
                p2 += 1

            if i % 2 == 1:
                p1 += 1

            set_chars.add(char)
            if last_len_pal == i - 1:
                # this means the last detected palindrome was the previous substring
                # then this new substring is a palindrome only and only if all characters so far are the same
                if len(set_chars) == 1:
                    last_len_pal += 1
                    pals.add(string[:i + 1])
                # no need to proceed to the next part
                continue

            tp1, tp2 = p1, p2
            # time to evaluate w
            while tp1 > -1 and tp2 <= i and string[tp1] == string[tp2]:
                tp1 -= 1
                tp2 += 1

            # at this point there 2 cases:
            # either p1 == -1 and p2 == len(string) which means the string is palindrome
            if tp1 == -1 and tp2 == i + 1:
                last_len_pal = i
                pals.add(string[: i + 1])

        return pals

    def countSubstrings(self, s: str) -> int:
        counter = 0
        for i in range(len(s)):
            counter += len(self.all_palindromes_start(s[i:]))
        return counter

    def maxProductNoZero(self, nums: list[int],
                         start_index: int,
                         end_index: int,
                         sign_dict: dict[int, list[int]]) -> int:

        nums = nums[start_index: end_index]
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]

        # first step is to count the number of negative numbers in this block
        count_neg = [i for i in sign_dict[-1] if start_index <= i < end_index]

        if len(count_neg) % 2 == 0:
            return math.prod(nums)

        total_product = math.prod(nums)

        if len(count_neg) == 1:
            neg_index = count_neg[0] - start_index
            p1, p2 = total_product // math.prod(nums[:neg_index + 1]), total_product // math.prod(nums[neg_index:])
            return max([p1, p2])

        # case: odd number of negative numbers
        first = count_neg[0]
        last = count_neg[-1]

        # each of them should be reduced with the start_index value
        last -= start_index
        first -= start_index

        first_part = math.prod(nums[:first + 1])
        second_part = math.prod(nums[last:])

        p1, p2 = total_product // first_part, total_product // second_part

        return max(p1, p2)

    def maxProduct(self, nums: List[int]) -> int:
        # let's first rule out some degenerate cases
        if len(nums) == 1:
            return nums[0]
        # first let's save the indices of values of each sign
        sign_indices = {-1: set(), 0: set(), 1: set()}
        for i, n in enumerate(nums):
            sign_indices[np.sign(n)].add(i)

        for k, v in sign_indices.items():
            sign_indices[k] = sorted(list(v))

        zeros = sign_indices[0]
        # first let's iterate through the zeros
        if len(zeros) > 0:  # if there is at least one zero element in the original array
            if len(zeros) == 1:
                zero_index = zeros[0]

                res1 = self.maxProductNoZero(nums, 0, zero_index, sign_indices)
                res2 = self.maxProductNoZero(nums, zero_index + 1, len(nums), sign_indices) if zero_index + 1 < len(
                    nums) else 0
                res = max(res1, res2)
            else:
                res = max([self.maxProductNoZero(nums, zeros[i] + 1, zeros[i + 1], sign_indices)
                           for i in range(len(zeros) - 1)])
                # there are 2 values forgotten so far: before the first zero, and after the last zero
                res = max(res, self.maxProductNoZero(nums, 0, zeros[0], sign_indices))
                res = max(res, self.maxProductNoZero(nums, zeros[-1] + 1, len(nums), sign_indices))
            # the final result should be at least 0: as arrays of similar structure
            # will return -1,0,-1,0,-1 negative numbers
            return max(0, res)
        return self.maxProductNoZero(nums, 0, len(nums), sign_indices)

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

    # well another medium, but it might not be as hard as the problem above:
    # https://leetcode.com/problems/coin-change/

    def innerCoinChange(self,
                        target: int,
                        coins: set,
                        min_coin: int,
                        memo: dict = None):
        memo = {} if memo is None else memo
        # base cases
        if target == 0:
            return 0

        if target < min_coin:
            return -1

        if target in coins:
            return 1

        if target in memo:
            return memo[target]

        res = float('inf')
        for c in coins:
            temp_res = self.innerCoinChange(target - c, coins, min_coin, memo)
            if temp_res != -1:
                res = min(res, temp_res)
                if res == 1:
                    break
        memo[target] = (res + 1) if res != float('inf') else -1
        return memo[target]

    def coinChange(self, coins: List[int], amount: int) -> int:
        min_coin = min(coins)
        coins = set(coins)
        return self.innerCoinChange(amount, coins, min_coin)

    def inner_decoding(self, string: str, mapping: set[str], memo: dict = None):
        memo = {} if memo is None else memo
        if len(string) == 0:
            return 0
        # some base cases
        if len(string) == 1:
            return int(string[0] in mapping)

        if len(string) == 2:
            return int(string in mapping) + int(string[0] in mapping and string[1] in mapping)

        if string in memo:
            return memo[string]

        # given a string, there 2 main approaches, either take the first character encode it
        # and get the count of string[1:]
        # or encode the first 2 characters and get the count of string[2:]

        two = None
        one = None
        if string[:1] in mapping:
            two = self.inner_decoding(string[2:], mapping, memo)
            memo[string[2:]] = two

        if string[0] in mapping:
            one = self.inner_decoding(string[1:], mapping, memo)
            memo[string[1:]] = one

        one = 0 if one is None else one
        two = 0 if two is None else two
        memo[string] = one + two
        return memo[string]

    def numDecodings(self, string: str) -> int:
        mapping = [str(n) for n in range(1, 27)]
        return self.inner_decoding(string, mapping)

    # well I need to go back to the decoding problem later...
    # let's tackle this one instead.
    def unique_paths(self, grid: List[List[int]], y: int, x: int, memo: dict = None):
        memo = {} if memo is None else memo
        # let's start with the base cases
        # leaving the grid
        if y >= len(grid) or x >= len(grid[0]):
            return 0
        # passing through an obstacle
        if grid[y][x] == 1:
            return 0
        # reaching the final position
        if y == len(grid) - 1 and x == len(grid[0]) - 1:
            return 1

        key = (y, x)
        if key in memo:
            return memo[key]

        memo[key] = self.unique_paths(grid, y + 1, x, memo) + self.unique_paths(grid, y, x + 1, memo)
        return memo[key]

    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        return self.unique_paths(obstacleGrid, 0, 0)

    # it would be safe to state that the problem above is a standard dynamic programming problem. Thus, I shouldn;t
    # feel so high and mighty after solving it.


if __name__ == '__main__':
    sol = Solution()
    s = "1201234"
    p = sol.numDecodings(s)
    print(p)
