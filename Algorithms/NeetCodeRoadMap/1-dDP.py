"""
This file contains my solutions for the leet code problems proposed in the 1d DP problems:
https://neetcode.io/roadmap
"""
from typing import List


# noinspection PyMethodMayBeStatic
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
