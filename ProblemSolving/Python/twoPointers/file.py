
def countDistinctSubarray(arr, n = None): 
    """
    https://www.geeksforgeeks.org/problems/equivalent-sub-arrays3731/1?page=1&category=two-pointer-algorithm&difficulty=Easy,Medium&status=unsolved&sortBy=accuracy
    Args:
        arr (_type_): _description_
        n (_type_): _description_
    """
    if n is None:
        n = len(arr)

    distinctNumbers = len(set(arr))

    occ_count = {}

    total_count = 0
    ptr1, ptr2 = 0, 0
    
    while (ptr2 < n):

        while (ptr2 < n):
            v = arr[ptr2]
            
            if v in occ_count:
                occ_count[v] += 1
            else:
                occ_count[v] = 1

            if len(occ_count) == distinctNumbers:
                break

            ptr2 += 1
            
        while len(occ_count) == distinctNumbers:
            total_count += n - ptr2
            
            v = arr[ptr1]
            occ_count[v] -= 1

            if occ_count[v] == 0:
                occ_count.pop(v)
            
            ptr1 += 1

        ptr2 += 1

    return total_count


def longestKSubstr(s: str, k: int):
    n = len(s)
    
    occ_count = {}

    ptr1, ptr2 = 0, 0
    
    max_length = -1

    while (ptr2 < n):

        while (ptr2 < n):
            v = s[ptr2]
            
            if v in occ_count:
                occ_count[v] += 1
            else:
                occ_count[v] = 1

            if len(occ_count) == k + 1:
                break

            ptr2 += 1
        
        if ptr2 == n and len(occ_count) != k:
            return max_length


        if ptr2 != n:
            # remove the element from the last ptr2
            occ_count.pop(s[ptr2])

        ptr2 = ptr2 - 1

        max_length = max(max_length, ptr2 - ptr1 + 1)

        while len(occ_count) == k:            
            v = s[ptr1]
            occ_count[v] -= 1

            if occ_count[v] == 0:
                occ_count.pop(v)
            
            ptr1 += 1

        ptr2 += 1

    return max_length


def minimumStepRec(n: int, memo=None):
    if memo is None:
        memo = {}
    
    if n <= 1:
        return 0
    
    if n in memo:
        return memo[n]
    
    if n % 3 == 0:
        return 1 + minimumStepRec(n // 3, memo=memo)
                       
    return 1 + minimumStepRec(n - 1, memo=memo)


def maxWeightCell(n, edges):
    weight_map = {}
    
    max_weight = 0
    best_index = n - 1

    for index, v in enumerate(edges):
        # this means the index is not pointing to another cell
        if v == -1:
            continue
        
        if v not in weight_map :
            weight_map[v] = 0
        
        weight_map[v] += index
        
        if weight_map[v] >= max_weight:
            max_weight = weight_map[v]

            best_index = v
    return best_index

if __name__ == '__main__':
    print(maxWeightCell(3, edges=[-1, -1, -1]))
