"""
This script contains my solutions for gfg problems that can be solved mainly using a hashmap or a set
"""

from typing import List
from collections import defaultdict, deque, Counter

# https://www.geeksforgeeks.org/problems/smallest-positive-missing-number-1587115621/1?page=1&category=Arrays&difficulty=Medium&status=unsolved&sortBy=submissions
def missingNumber(arr: List[int]) -> int:
    # basically convert all positive numbers into a set and iterate from 1 
    pos_nums_set = set()
    max_element = -float("inf")
    
    for v in arr:
        if v >= 1:
            pos_nums_set.add(v)
        max_element = max(max_element, v)

    # if all element are non-positive, then return 1
    if max_element < 1:
        return 1

    # otherwise iterate from "1" to "max_element + 1", the last number if a guaranteed miss
    for i in range(1, max_element + 2):
        if i not in pos_nums_set:
            return i


# https://www.geeksforgeeks.org/problems/array-pair-sum-divisibility-problem3257/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

# 1st check: must have an even number of element 
# save the count of elements with each reminder: {i: {# v | v % k = i }}

def canPair(nums: List[int], k: int):
    if len(nums) % 2 == 1:
        return False
    
    k_nums = [v % k for v in nums]
    
    k_map = dict([(v, 0) for v in k_nums])

    for v in k_nums:
        k_map[v] += 1

    # element divisible by "k" are associated together: need an even count of such numbers
    if 0 in k_map and  k_map[0] % 2 == 1:
        return False

    # if k is even then numbers with reminder k // 2 are grouped together, need an even count of such numbers
    if (k % 2 == 0) and (k // 2) in k_map and (k_map[k // 2] % 2 == 1):
        return False
    
    # for other reminders, then r and k - r need to be grouped together, the total count for each of those reminders must be the same
    for rem, _ in k_map.items():
        other_rem = (k - rem) % k
        
        if (other_rem not in k_map) or (k_map[other_rem] != k_map[rem]):
            return False
        
    return True


# going through few problems from this list: 
# https://www.geeksforgeeks.org/hashing-data-structure/?ref=lbp
# some of them are just dumb...

# somehow this problem has an accuracy of 30%
# https://www.geeksforgeeks.org/problems/incomplete-array3859/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
def countElements(n: int, a: List[int]) -> int:
    min_val, max_val = a[0], a[0]
    for v in a: 
        min_val = min(min_val, v)
        max_val = max(max_val, v)

    return max_val - min_val + 1 - len(set(a))


"""
https://www.geeksforgeeks.org/problems/count-distinct-elements-in-every-window/1
"""
def countDistinct(arr, n, k):
    counter = {}
    for v in arr[:k]:
        if v not in counter:
            counter[v] = 0
        counter[v] += 1
    
    res = [0 for _ in range(n - k + 1)]
    res[0] = len(counter)

    for i in range(k, n):
        val_remove = arr[i - k]
        val_add = arr[i]

        # add val_add
        if val_add not in counter:
            counter[val_add] = 0
        
        counter[val_add] += 1
        
        counter[val_remove] -= 1
        if counter[val_remove] == 0:
            del(counter[val_remove])

        res[i - k + 1] = len(counter)

    return res


# https://www.geeksforgeeks.org/problems/find-rectangle-with-corners-as-1--141631/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card 
def ValidCorner(matrix: List[List[int]]): 
    # iterate thorugh
    pass


# a problem from neetcode.io: https://neetcode.io/problems/string-encode-and-decode
from typing import List
def encode(strs: List[str]) -> str:
    if len(strs) == 0:
        return ""
    
    encoded_list = ["_".join([str(ord(c)) for c in s]) if len(s) > 0 else "" for s in strs]
    return "*" + "*".join(encoded_list)
    
def decode(string: str) -> List[str]:
    if len(string) == 0:
        return []
    
    string = string[1:]
    l = string.split("*")
    return ["".join([chr(int(c)) for c in s.split("_")]) if len(s) > 0 else "" for s in l ]


"""
https://www.geeksforgeeks.org/problems/largest-subarray-of-0s-and-1s/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
"""
def maxLen(arr, N=None):
    if N is None:
        N = len(arr)
    # my solution combines the idea of hashing and PrefixSum array
    count0 = 0
    count1 = 0
    prefixSum = [0 for _ in arr]
    max_len = 0
    for index, val in enumerate(arr):
        count0 += int(val == 0)
        count1 += int(val == 1) 
        prefixSum[index] = count1 - count0
        
        if count0 == count1:
            max_len = index + 1

    if max_len == N:
        return N

    pfs_indices = defaultdict(lambda:[])

    for index, val in enumerate(prefixSum):
        pfs_indices[val].append(index)
    
    for _, v in pfs_indices.items():
        max_len = max(max_len, abs(v[0] - v[-1]))
    
    return max_len


"""
https://www.geeksforgeeks.org/problems/count-pairs-with-given-sum5022/1
"""
def getPairsCount(arr, target):
    # get the frequencies of each element in the arrya
    freqs = defaultdict(lambda : 0)
    count = 0

    for val in arr:
        freqs[val] += 1

    for val in arr:
        new_t = target - val
        if new_t == val:
            count += (freqs[val] - 1) / 2
        else:
            count += freqs[new_t] / 2
    
    return int(count)

"""
https://www.geeksforgeeks.org/problems/first-repeating-element4018/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
"""
def firstRepeated(arr):
    freqs = {}
    q = deque()
    for index, val in enumerate(arr):
        if val not in freqs:
            freqs[val] = 0
            q.append((val, index))
        freqs[val] += 1
    
    while len(q) > 0 and freqs[q[0][0]] == 1:
        q.popleft()
    
    if len(q) == 0:
        return -1

    return q[0][1] + 1


# Although this problem is already solved, I see it as a great example of combining the Dict and Queue data structures: 
"""
https://www.geeksforgeeks.org/given-a-string-find-its-first-non-repeating-character/#efficient-approach-1-using-hash-map-on-time-and-o1-auxiliary-space
"""

# let's start with the first efficient solution
def first_not_repeat_char_2_traversals(string: str) -> int:
    # the first natural idea it to compute the frequency of each character: first iteration
    # iterate again: consult the frequency of each char, if it is 1: return else, return -1 at the end...
    freqs = {}
    for c in string:
        if c not in freqs:
            freqs[c] = 0
        freqs[c] += 1
    
    for c in string:
        if freqs[c] == 1:
            return c
    return -1

# this is a better solution with only on string traversal
def first_not_repeat_char_1_traversal(string: str) -> int:
    # my main line of thought before solving this question was: assuming at each step I am saving the current first character 
    # occuring once so far in the string, how can I get the next char with only one occurrence once the current save char is repeated
    
    ## well you've guessed it a queue !!!

    freqs = {}
    # the queue point here is that queue should save only characters with frequency 1 (in order)
    queue = deque()

    for c in string: 
        if c not in freqs:
            queue.append(c)
            freqs[c] = 0
        
        freqs[c] += 1
        # the two lines below ensure that the queue contains
        # only characters that appear exactly once
        # + the FIFO nature of the queue ensures that the first element in the queue appears first in the STRING !!! 
        while len(queue) > 0 and freqs[queue[0]] != 1:
            queue.pop()
    
    return queue[0] if len(queue) else -1


"""
https://www.geeksforgeeks.org/problems/longest-consecutive-subsequence2449/1
"""
def findLongestConseqSubseq(array, N = None):
    if N is None:
        N = len(array)
    arr = set(array)
    visited = dict([(a, False) for a in arr])

    max_len = 0
    for v in arr:
        if visited[v]:
            continue 
        
        # v has not been visited below
        start = v - 1
        while start in arr:
            start = start - 1
        
        start = start + 1
        counter = 0
        while start in arr:
            visited[start] = True
            start += 1
            counter += 1

        max_len = max(counter, max_len)

    return max_len


# https://www.geeksforgeeks.org/problems/kth-distance3757/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
def checkDuplicatesWithinK(arr: List[int], k: int):
    # basically we need to find if there is an element for which there exists i, j such that arr[i] == arr[j] and abs(i - j) <= k

    # using a hashmap is probably the first idea that comes to mind...    
    # associate each number with the last occurrence if a new occurrence is detected, basically check the distance between the indices

    val_indices = {}

    for i, v in enumerate(arr):
        if v in val_indices:
            if i - val_indices[v] <= k:
                return True
        # update val_indices anyway
        val_indices[v] = i
    
    return False


# this is a very simple problem: 
# https://www.geeksforgeeks.org/problems/remove-duplicates-in-small-prime-array/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card 
def removeDuplicates(arr: List[int]):
    arr_set = set(arr)
    n = len(arr_set)
    
    arr_set.clear()
    
    new_arr = [0 for _ in range(n)]
    counter = 0

    for v in arr:
        if v not in arr_set:
            arr_set.add(v)
            new_arr[counter] = v
            counter += 1
    
    return new_arr
    

# the simplest DSA question ever...
def isSubset( a1, a2, n=None, m=None):
    c1, c2 = Counter(a1), Counter(a2)
    for k, v in c2.items():
        if k not in c1:
            return False
        if v > c1[k]:
            return False
    return True


# this question for some reason has an 18% accuracy percetange (I mean, it is a waste of time to do, if one reaches a certain level)
def findDuplicates(arr: List[int]):
    d = {}
    count = 0
    for v in arr:
        if v not in d:
            d[v] = 0

        if d[v] == 1:
            count += 1
        
        d[v] += 1

    res = [0 for _ in range(count)]

    i = 0
    for k, freq in d.items():
        if freq > 1: 
            res[i] = k
            i += 1
    
    return res



def findTwoElement(arr: List[int]):
    n = len(arr)
    arr_set = set(arr)
    missing = 0 

    for v in range(1, n + 1):
        if v not in arr_set:
            missing = v
            break
    
    # find the repeating number
    diff = (n * (n + 1)) // 2 - sum(arr)
    repeating = missing - diff
    return repeating, missing

