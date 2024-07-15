"""
https://www.geeksforgeeks.org/problems/smallest-subarray-with-sum-greater-than-x5651/1
"""

def smallestSubWithSum(x, arr):
    n = len(arr)
    start, end = 0, 1
    
    min_len = float('inf')
    
    current_sum = arr[start]
    while end < n:
        while end < n and arr[end] >= 0 and current_sum <= x:
            current_sum += arr[end]
            end += 1
        
        if end == n and current_sum <= x:
            break

        if current_sum <= x:  
            # this means that arr[end] is negative
            start = end + 1 
            end = start + 1
            continue
        
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
