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




if __name__ == '__main__':
    nums = [2, 2, 8, 20, 10]
    sol = Solution()
    v = sol.rob(nums)
    print(v)