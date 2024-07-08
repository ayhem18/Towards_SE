# once again another "greedy" problem in the "dp" section
def maxSubstring(string):
    """
    https://www.geeksforgeeks.org/problems/longest-increasing-subsequence-1587115620/1?page=1&difficulty=Medium&status=unsolved&sortBy=submissions
    """
    n = len(string)
    best_start, best_end = 0, 0
    count = 0
    best_count = -1
    start, end = 0, 0

    while end < n:
        count += (2 * (string[end] == '0') - 1)

        if count >= best_count:
            best_count = count
            best_start = start
            best_end = end

        if count <= 0:   
            start = end + 1
            count = 0
        
        end += 1
        

    # if count > best_count:
    #     best_count = count
    #     best_start = start
    #     best_end = end

    return best_start, best_end, best_count
