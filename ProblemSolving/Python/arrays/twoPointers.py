"""
Well classifying problems is a bit difficult
"""

# https://www.geeksforgeeks.org/problems/maximum-index-1587115620/1?page=1&category=Arrays&difficulty=Medium&status=unsolved&sortBy=submissions

from typing import List


# the algorithm below doesn't woek
def maxIndexDiff(a :List[int]):
    maxs = {}
    mins = {}

    counter = 0
    n = len(a)

    while counter + 1 < n:

        initial = counter
        while counter + 1 < n and a[counter] <= a[counter + 1]:
            counter += 1
        
        if counter != initial:
            mins[len(mins)] = initial

        # save the maximum value
        maxs[len(maxs)] = counter

        # at this point we know that a[counter] > a[counter + 1]
        while counter + 1 < n and a[counter] > a[counter + 1]:
            counter += 1

    mins = [mins[i] for i in range(len(mins))]
    maxs = [maxs[i] for i in range(len(maxs))]

    if len(mins) == 0: # which means that sequence is decreasing
        return 0


    i1, i2 = 0, len(maxs) - 1

    while True:
        if a[mins[i1]] <= a[maxs[i2]]:
            return maxs[i2] - mins[i1]
        
        next2 = i2
        next1 = i1

        while next2 >= 0 and a[maxs[next2]] <= a[maxs[i2]]:
            next2 -= 1

        while next1 < len(mins) and a[mins[next1]] >= a[mins[i1]]:
            next1 += 1

        # consider the possible candidates
        candidates = []

        if a[mins[next1]] <= a[maxs[next2]]:
            candidates.append((next1, next2))

        if a[mins[i1]] <= a[maxs[next2]]:
            candidates.append((i1, next2))

        if a[mins[next1]] <= a[maxs[i2]]:
            candidates.append((next1, i2))

        if len(candidates) > 0:
            index1, index2 = max(candidates, key=lambda x: maxs[x[1]] - mins[x[0]])
            return maxs[index2] - mins[index1]

        i1 = next1
        i2 = next2

