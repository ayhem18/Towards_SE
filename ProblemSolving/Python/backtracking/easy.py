from math import factorial, ceil
from copy import copy
from standard import choose_k_from_set


# even though this function works, regardless of the input
# it will return a large number of duplicate sets in case
# of duplicate numbers in

def __all_paths( n: int, m: int, grid, current_position):
    if current_position == (n - 1, m - 1):
        return [[grid[n - 1][m - 1]]]

    # find the possible next positions
    next_pos = []
    y, x = current_position
    if y + 1 < n:
        next_pos.append((y + 1, x))

    if x + 1 < m:
        next_pos.append((y, x + 1))

    res = []
    for pos in next_pos:
        temp = __all_paths(n, m, grid, pos)
        for i in range(len(temp)):
            temp[i] = [grid[y][x]] + temp[i]
        res.extend(temp)
    return res

def findAllPossiblePaths( n: int, m: int, grid):
    return __all_paths(n, m, grid, (0, 0))

# this is my attempt to solve:
# https://practice.geeksforgeeks.org/problems/combination-sum-iii/1?page=1&category[]=Backtracking&sortBy=accuracy
# let's start with some inner methods



def combinationSum( k, target):
    temp = choose_k_from_set(nums=list(range(1, 10)), k=k)
    return [t for t in temp if sum(t) == target]

def permute_str( string: str, k: int):
    if len(string) == 0 or k == 1:
        return string

    n = len(string)
    fac_n = factorial(n)
    k = k % fac_n
    k = fac_n if k == 0 else k
    fac_n1 = fac_n // n
    rotation_factor = int(ceil(k / fac_n1)) - 1
    new_str = string[:rotation_factor] + string[rotation_factor + 1:]
    result = string[rotation_factor] + permute_str(new_str, k % fac_n1)
    return result

def kthPermutation( n: int, k: int) -> str:
    string = ''.join([str(i) for i in range(1, n + 1)])
    return permute_str(string, k)

# the next problem is:
# https://practice.geeksforgeeks.org/problems/permutations-of-a-given-string2041/1?page=1&category[]=Backtracking&sortBy=submissions
def inner_find_permutation( s):
    # let's start with some base cases:
    if len(s) <= 1:
        return [s]
    if len(s) == 2:
        return list({s[0] + s[1], s[1] + s[0]})

    res = []
    for i in range(len(s)):
        new_str = s[:i] + (s[i + 1:] if i + 1 < len(s) else '')
        temp = inner_find_permutation(new_str)
        # add the i-th character to the beginning of each string in the temp list
        for j in range(len(temp)):
            temp[j] = s[i] + temp[j]
        res.extend(temp)
    return res

def find_permutation( s):
    return sorted(list(set(inner_find_permutation(s))))

def InnerCombs(self, nums, target: int):
    # this function assumes the input is sorted
    if target < nums[0]:
        return []
    # the next base case
    if len(nums) == 1:
        return [[nums[0] for _ in range(target // nums[0])]] if target % nums[0] == 0 else []

    min_num = nums[0]
    max_times = target // min_num
    res = []

    for i in range(max_times + 1):
        new_target = target - min_num * i
        current_list = [min_num for _ in range(i)]
        if new_target == 0:
            res.append(current_list)
        elif new_target > 0:
            temp = InnerCombs(nums[1:], new_target)
            if len(temp) > 0:
                for j in range(len(temp)):
                    temp[j] = current_list + temp[j]
                res.extend(temp)
    return res

def combinationalSum(self, nums, target):
    nums = sorted(list(set(nums)))
    if len(nums) == 0:
        return []

    res = InnerCombs(nums, target)
    return sorted(res, key=lambda x: tuple(x))

def combination_of_sets(self, sets):
    # sets is a list of lists
    if len(sets) == 1:
        return sets[0]
    res = []
    sub_combination = combination_of_sets(sets[1:])
    for string in sets[0]:
        temp = copy(sub_combination)
        for j in range(len(temp)):
            temp[j] = string + temp[j]
        res.extend(temp)
    return res

phone = {2: ['a', 'b', 'c'],
            3: ['d', 'e', 'f'],
            4: ['g', 'h', 'i'],
            5: ['j', 'k', 'l'],
            6: ['m', 'n', 'o'],
            7: ['p', 'q', 'r', 's'],
            8: ['t', 'u', 'v'],
            9: ['w', 'x', 'y', 'z']}

def possibleWords(self, a, _):
    # first build the sets
    sets = [phone[v] for v in a]
    return combination_of_sets(sets)

