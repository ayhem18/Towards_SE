from typing import List
from collections import defaultdict

def longestSubseq(n : int, a : List[int]) -> int:    
    """
    https://www.geeksforgeeks.org/problems/longest-subsequence-such-that-difference-between-adjacents-is-one4724/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
    """
    val2index = defaultdict(lambda :[])
    for i, v in enumerate(a):
        val2index[v].append(i)

    dp = [-1 for _ in range(n)]
    # the longuest subsequence ending at index = 0, is of length 1
    dp[0] = 1

    res = 0

    # for index in range(1, n + 1):
    for i, val in enumerate(a[1:],start=1):
        plus = val2index[val + 1]
        minus = val2index[val - 1]

        plus = [j for j in plus if j < i]
        minus = [j for j in minus if j < i]
        add_plus = 0 if len(plus) == 0 else max([dp[j] for j in plus])
        add_minus = 0 if len(minus) == 0 else max([dp[j] for j in minus])

        dp[i] = 1 + max(add_minus, add_plus)
        res = max(dp[i], res)

    return res


"""
https://leetcode.com/problems/longest-increasing-subsequence/
"""
def lengthOfLIS(nums):
    seq_end_at_i = [1 for _ in nums]
    # the idea here is to proceed with caution
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                seq_end_at_i[i] = max(seq_end_at_i[i], seq_end_at_i[j] + 1)
    
    return max(seq_end_at_i)


def _isSubsetSum(nums, sum, n, memo):
    if sum <= 0:
        return False

    # consider the base case
    if n == 1:
        return nums[0] == sum

    if memo[sum][n] != -1:
        return memo[sum][n]
    
    if sum == nums[n - 1]:
        return True

    res = _isSubsetSum(nums, sum - nums[n - 1], n - 1, memo) or _isSubsetSum(nums, sum, n - 1, memo)
    memo[sum][n] = res
    return res

def isSubsetSum(nums, sum):
    n = len(nums)
    dp = [[-1 for _ in range(n + 1)] for _ in range(sum + 1)]
    return _isSubsetSum(nums, sum, n, dp)


"""
https://leetcode.com/problems/partition-equal-subset-sum/
"""
def canPartition(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """ 
    array_sum = sum(nums)
    if array_sum % 2 != 0:
        return False

    target = array_sum // 2
    return isSubsetSum(nums, target)






"""
https://leetcode.com/problems/decode-ways/
"""
def _numDecodings(string, n, memo):
    if n == 1:
        return int(string[0] != '0') 

    if n == 0:
        return 1

    if memo[n] != -1:
        return memo[n]
    
    c1 = 0
    c2 = 0
    if string[n - 1] != '0':
        c1 = _numDecodings(string, n - 1, memo)
    if (1 <= int(string[n - 2: n]) <= 26) and string[n - 2] != '0':
        c2 = _numDecodings(string, n - 2, memo)

    res = c1 + c2
    memo[n] = res
    return res 

def numDecodings(s: str):
    n = len(s)
    memo = [-1 for _ in range(n + 1)]
    memo[0] = 0
    memo[1] = int(s[0] != '0')
    return _numDecodings(s, n, memo)

if __name__ == '__main__':
    s="106123"
    print(numDecodings(s))
