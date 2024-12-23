"""
This script contains my solutions for problems that can be solved based on the Kadanes algorithm
"""

def maxSubArraySum(arr):
    """
    https://www.geeksforgeeks.org/problems/kadanes-algorithm-1587115620/1?page=1&difficulty=Medium&status=unsolved&sprint=50746f92a895c22a50504ac0c1fb9c84&sortBy=submissions
    """
    n = len(arr)
    best_sum = -float('inf')
    i, j = 0, 0
    while i < n:
        current = arr[i]
        j = i + 1
        
        best_sum = max(current, best_sum)
        
        while j < n and current >= 0:
            current += arr[j]
            j += 1
            best_sum = max(best_sum, current)

        # set 'i' to 'j'
        i = j

    return best_sum


def maxSubArrayNaive(array):
    best_sum = -float('inf')
    n = len(array)
    for i in range(n):
        for j in range(i, n):
            best_sum = max(best_sum, sum(array[i:j + 1]))
    return best_sum
