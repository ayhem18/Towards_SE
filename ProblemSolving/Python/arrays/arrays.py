"""
This file contains my solutions for some problems on 'arrays'
"""

def longSubarrWthSumDivByK (arr: list[int],  n: int, K) : 
    """
    https://www.geeksforgeeks.org/problems/longest-subarray-with-sum-divisible-by-k1259/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article 
    """

    total = 0
    prefixSum = arr.copy()
    for i, v in enumerate(arr):
        total += v
        prefixSum[i] = (total % K)

    max_len = -1
    for i, v in enumerate(prefixSum):
        if v == 0:
            max_len = i + 1
    
    # if the entire array has a sum divisible by 'K', then return already
    if max_len == n:
        return n

    mods_indices = {}
    for i, v in enumerate(prefixSum):
        if v in mods_indices:
            mods_indices[v][1] = i
        else:
            mods_indices[v] = [i, -1]

    for _, pair in mods_indices.items():
        if pair[1] != -1:
            max_len = max(max_len, pair[1] - pair[0])

    return max_len



if __name__ == '__main__':
    arr = [-2, 2, -5, 12, -11, -1, 7]
    print(longSubarrWthSumDivByK(arr, -1, 3))
