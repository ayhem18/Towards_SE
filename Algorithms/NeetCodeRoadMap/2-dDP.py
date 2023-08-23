"""
This script contains my solutions for the 2-d DP problems listed in the NeetCode Roadmap
"""
from typing import List, Dict


# noinspection PyMethodMayBeStatic
class Solution:
    def target_ways(self,
                    nums: List[int],
                    target: int,
                    sums_dict: Dict[int, int],
                    memo: Dict[tuple[int, int], int] = None) -> int:
        # sums_dict: maps each index to the sum of numbers starting from that index in the original array
        # nums is assumed to be sorted
        if memo is None:
            memo = {}

        if len(nums) == 1:
            return int(nums[0] == abs(target))

        sum_left = sums_dict[len(nums)]

        if abs(target) > sum_left or (abs(target) - sum_left) % 2 != 0:
            return 0
        if abs(target) == sum_left:
            return 2 ** len([v for v in nums if v == 0])

        key = (len(nums), target)

        if key in memo:
            return memo[key]

        memo[key] = self.target_ways(nums[1:], target - nums[0], sums_dict, memo) + \
                    self.target_ways(nums[1:], target + nums[0], sums_dict, memo)

        return memo[key]

    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        # first sort the nums
        nums = sorted(nums)
        # second, build the sums_dict
        sums_dict = {}
        count = 0
        for i in range(len(nums)):
            count += nums[len(nums) - i - 1]
            sums_dict[i + 1] = count

        return self.target_ways(nums, target, sums_dict)

    def maxProfit(self, prices: List[int]) -> int:
        # we will solve the problem with tabulation
        values = [0 for _ in prices]
        if len(prices) < 2:
            return 0

        values[1] = max(0, prices[1] - prices[0])
        for i in range(2, len(values)):
            no_sell_last = values[i - 1]
            best_sell_mid = 0
            for k in range(i - 1, 1, -1):
                best_sell_mid = max(best_sell_mid, prices[i] - prices[k] + values[k - 2])
            sell_last_buy_first = prices[i] - prices[0]
            values[i] = max([no_sell_last, best_sell_mid, sell_last_buy_first])

        return values[-1]

    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # let's create out grid
        values = [[0 for _ in range(len(text2) + 1)] for _ in range(len(text1)+1)]
        for i, c1 in enumerate(text1, 1):
            for j, c2 in enumerate(text2, 1):
                op1 = int(c1 == c2) + values[i - 1][j - 1]
                op2 = values[i - 1][j]
                op3 = values[i][j - 1]
                values[i][j] = max([op1, op2, op3])
        return values[-1][-1]




if __name__ == '__main__':
    sol = Solution()
    t1 = 'abcde'
    t2 = 'acde'
    print(sol.longestCommonSubsequence(t1, t2))