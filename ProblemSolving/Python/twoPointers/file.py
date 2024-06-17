
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



if __name__ == '__main__':
    string = "aaaaabba"
    
    for k in range(1, len(string)):
        print(f"k : {k} -> {longestKSubstr(string, k=k)}")
