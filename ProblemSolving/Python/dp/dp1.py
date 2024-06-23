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
 


if __name__ == '__main__':
    a = [2, 8, 5, 1, 10, 5, 9, 9, 3,5]
    n = len(a)
    print(longestSubseq(n, a))
