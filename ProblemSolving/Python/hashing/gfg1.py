"""
This is my attempt to learn the most important ideas / tricks about the hash data structure based on the problems suggested by GFG

https://www.geeksforgeeks.org/top-50-problems-on-hash-data-structure-asked-in-sde-interviews/ 

"""

from collections import deque

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

from collections import defaultdict
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

from collections import Counter
def majorityElement(A, N):
    maj_thresh = N // 2 + 1
    c = Counter(A)
    max_count = 0
    max_val = 0
    for k, v in c.items(): 
        if v > max_count: 
            max_count = v
            max_val = k

    if max_count >= maj_thresh:
        return max_val
    return -1


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
https://www.geeksforgeeks.org/problems/array-pair-sum-divisibility-problem3257/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
"""
def canPair(nums, k):
    if len(nums) % 2 == 1:
        return False
    
    k_nums = [v % k for v in nums]
    
    k_map = dict([(v, 0) for v in k_nums])

    for v in k_nums:
        k_map[v] += 1

    if 0 in k_map and  k_map[0] % 2 == 1:
        return False
    
    if (k % 2 == 0) and (k // 2) in k_map and (k_map[k // 2] % 2 == 1):
        return False
    
    for rem, _ in k_map.items():
        other_rem = (k - rem) % k
        
        if (other_rem not in k_map) or (k_map[other_rem] != k_map[rem]):
            return False
        
    return True



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

