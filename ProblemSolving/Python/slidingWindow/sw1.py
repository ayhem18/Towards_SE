"""
https://www.geeksforgeeks.org/problems/smallest-subarray-with-sum-greater-than-x5651/1
"""

def smallestSubWithSum(x, arr):
    # it is known that all elements are non-negative
    n = len(arr)
    start, end = 0, 1
    
    min_len = float('inf')
    
    current_sum = arr[start]
    while end < n:
        while end < n and current_sum <= x:
            current_sum += arr[end]
            end += 1
        
        if end == n and current_sum <= x:
            break

        # ignore the last element anyway
        end = end - 1
        while current_sum > x:
            current_sum -= arr[start]
            start += 1

        start = start - 1
        min_len = min(min_len, end - start + 1)
        start += 1
        end = end + 1

    if min_len == float('inf'):
        return 0

    return min_len

"""
https://www.geeksforgeeks.org/problems/max-sum-subarray-of-size-k5313/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
"""
def maximumSumSubarray (k,arr,n=None):
    if n is None:
        n = len(arr)
    # the maximum sum of a sub-array of size K
    current_sum = sum(arr[:k])
    max_sum = current_sum
    for i in range(k, n):
        current_sum += arr[i]
        current_sum -= arr[i - k]
        max_sum = max(max_sum, current_sum)
    return max_sum


"""
https://www.geeksforgeeks.org/problems/maximum-of-all-subarrays-of-size-k3101/1
"""
## not solved yet !!

"""
https://www.geeksforgeeks.org/problems/length-of-the-longest-substring3036/1
"""
def longestUniqueSubsttr(string):
    n = len(string)
    unique_chars = set([string[0]])
    start, end = 0, 1
    max_len = 1
    while end < n:
        while end < n and string[end] not in unique_chars:
            unique_chars.add(string[end])
            end += 1
        
        max_len = max(max_len, end - start)
        
        if end == n:
            break

        while string[start] != string[end]:
            unique_chars.remove(string[start])
            start += 1

        # at this point we know string[start] == string[end] 
        unique_chars.remove(string[start])
        start = start + 1
            
    return max_len

        
