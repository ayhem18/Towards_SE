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


"""
https://leetcode.com/problems/jump-game/
"""
def canJump(arr, n = None):
    if n is None:
        n = len(arr)

    count = 1
    index = 0
    current_limit = arr[0]

    if current_limit >= n - 1:
        return True

    while index < n:
        next_limit = current_limit
        
        while index <= current_limit:
            next_limit = max(next_limit, arr[index] + index)
            next_limit = min(next_limit, n - 1)
            index += 1
    
        if index == n:
            return True

        if next_limit == current_limit:
            # this means, it is not possible to move further
            return False

        current_limit = next_limit
        count += 1
    
    return True


"""
https://leetcode.com/problems/jump-game-ii/description/
"""
def jump(arr):
    n = len(arr)

    count = 1
    index = 0
    current_limit = arr[0]

    if current_limit >= n - 1:
        return 1

    while index < n:
        next_limit = current_limit
        
        while index <= current_limit:
            next_limit = max(next_limit, arr[index] + index)
            next_limit = min(next_limit, n - 1)
            index += 1
    
        if index == n:
            return count

        if next_limit == current_limit:
            # this means, it is not possible to move further
            return -1

        current_limit = next_limit
        count += 1
    
    return count


"""
https://leetcode.com/problems/gas-station/
"""
def canCompleteCircuit(gas, cost):
    tank = 0
    diff = [g - c for g, c in zip(gas, cost)]
    start, end = 0, 0
    n = len(gas)

    if n == 1:
        return 0

    while end < n:
        tank += diff[end]
        if tank < 0:
            start = end + 1
            tank = 0
        end += 1

    if tank < 0:
        # this mean we could not go from (n - 1)-th station back to 0-th station
        return -1
    # we have enough tank to go from 'start' to 'n - 1' and then to 0
    end = 0
    while end < start:
        tank += diff[end]
        
        if tank < 0:
            return -1
        
        end += 1

    return start

"""
https://leetcode.com/problems/hand-of-straights/
"""
def isNStraightHand(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False 

    # let's build our counter
    counter = {}
    for v in hand:
        if v not in counter:
            counter[v] = 0
        counter[v] += 1

    sorted_values = sorted(list(set(hand)))
    min_value = sorted_values[0]
    min_value_index = 0

    while len(counter) > 0:
        copy_min_value = min_value
        for i in range(0, groupSize):
            val = copy_min_value + i
            if val not in counter:
                return False
            # this means that 'val' has been added to one group
            counter[val] -= 1
            
            if counter[val] == 0:
                # this means that we consumed all instances of the value 'val'
                del(counter[val])
            else: 
                # the value 'val' is still in the array
                # we need to update the minimum value in the array
                if min_value == copy_min_value and copy_min_value not in counter:
                    min_value = val
                    min_value_index += i
        
        if min_value == copy_min_value and min_value not in counter:
            min_value_index += groupSize
            if min_value_index < len(sorted_values):
                min_value = sorted_values[min_value_index]

    return True


"""
https://leetcode.com/problems/merge-triplets-to-form-target-triplet/
"""

def mergeTriplets(triplets, target):
    bool_flag = [False for _ in target]
    candidates = set()
    for c in triplets:
        add_c = True
        for vc, vt in zip(c, target):
            if vc > vt:
                add_c = False
                break
        if add_c:

            for i, (vc, vt) in enumerate(zip(c, target)):
                if vc == vt:
                    bool_flag[i] = True

            candidates.add(tuple(c))

    return len(candidates) > 0 and all(bool_flag)


"""
https://leetcode.com/problems/partition-labels/
"""
def partitionLabels(s):
    # let's get some of these ideas
    n = len(s)
    # let's first build the map  between the characters and their first and second position
    map_char_positions = {}
    for i, char in enumerate(s):
        if char not in map_char_positions:
            map_char_positions[char] = [i, i]
        else:
            # only the second position is modified: the last occurence of the 'char' in the string
            map_char_positions[char][-1] = i
    
    start, end = 0, 0
    limit = 0 
    
    parts = [0 for _ in range(n)]
    counter = 0

    while end < n:
        while end <= limit:
            # limit always <= n - 1
            limit = max(limit, map_char_positions[s[end]][-1])
            end += 1
        # at this point we know that every char in [start, end (included)] do not appear in the substring s[end + 1:]
        # we can save this as a part
        parts[counter] = end - start # keep in mind that "end == limit + 1" at this point of the program
        start = end
        counter += 1

        if end < n:
            limit = map_char_positions[s[end]][-1]
    
    final_res = [v for v in parts if v != 0]
    return final_res


def checkValidString(s):
    max_count = 0
    min_count = 0
    for char in s:
        if char == '(':
            max_count += 1 
            min_count += 1
        elif char == ')':
            max_count -= 1 
            min_count -= 1
        else:
            max_count += 1
            min_count -= 1
        if max_count < 0:
            return False
        
    return min_count <= 0 <= max_count

if __name__ == '__main__':
    s = '(**))'
    print(checkValidString(s))
