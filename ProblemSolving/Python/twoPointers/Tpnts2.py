from typing import List

"""
https://leetcode.com/problems/container-with-most-water/
"""
def maxArea(height: List[int]) -> int:
    # the amount of water stored between i and j is: min(height[i], height[j]) * abs(i - j) 
    # start, end indices
    n = len(height)
    p1, p2 = 0, n - 1    
    
    maw = 0
    while p1 < p2:
        maw = max(maw, min(height[p1], height[p2]) * (p2 - p1)) 
        if height[p1] <= height[p2]:
            p1 += 1
        else:
            p2 -= 1
    
    return maw

"""
https://leetcode.com/problems/trapping-rain-water/
"""
def trap(h: List[int]) -> int:
    # this code is still missing some parts !!!

    # let's get this bad boy out of the way
    n = len(h)
    if n <= 2:
        return 0 
    
    start, end = 0, 1
    increasing = h[end] >= h[start]
    total_water = 0

    highest = [0 for _ in range(n)]
    ishighest = [True for _ in range(n)]

    highest[-1] = h[-1]
    ishighest[-1] = True
    for i in range(n - 2, -1, -1):
        highest[i] = max(highest[i + 1], h[i])
        ishighest[i] = highest[i] > highest[i + 1]


    while end < n:
        increasing = increasing and h[start] <= h[end]
        if h[end] >= h[start]:
            if increasing:
                start = end
            else:
                block_water = h[start] * (end - start - 1)
                for v in h[start + 1 : end]:
                    block_water -= v
                total_water += block_water
                increasing = True                
                start = end

                while start < n and ishighest[start]:
                    start += 1
                
                end = start
        end += 1
    
        # while end < n and highest[end] == h[end]:
        #     end += 1
        
        # if end == n:
        #     break

    return total_water
