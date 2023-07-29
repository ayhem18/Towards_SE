"""
This file contains my solutions for the leet code problems proposed in the 1d DP problems:
https://neetcode.io/roadmap
"""
from typing import List


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
        # let's to tweak the problem just a tiny bit
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


if __name__ == '__main__':
    sol = Solution()
    string = 'a'
    print(sol.countSubstrings(string))
