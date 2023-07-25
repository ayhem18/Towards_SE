from math import factorial, ceil
from copy import copy
from itertools import chain


# noinspection PyMethodMayBeStatic,PyShadowingNames,SpellCheckingInspection
class Solution:
    def kSubsets(self, nums: list[int], k: int) -> list[list[int]]:
        if len(nums) == 0 or k == 0:
            return [[]]
        if k == 1:
            return [[v] for v in nums]

        res = []
        for index, v in enumerate(nums[:len(nums) - k + 1]):
            temp = self.kSubsets(nums[index + 1:], k - 1)
            # add the current value
            for i in range(len(temp)):
                temp[i] = [v] + temp[i]
            res.extend(temp)
        return res

    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = [self.kSubsets(nums, i) for i in range(len(nums) + 1)]
        res = list(chain(*res))
        return res

    def __all_paths(self, n: int, m: int, grid, current_position):
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
            temp = self.__all_paths(n, m, grid, pos)
            for i in range(len(temp)):
                temp[i] = [grid[y][x]] + temp[i]
            res.extend(temp)
        return res

    def findAllPossiblePaths(self, n: int, m: int, grid):
        return self.__all_paths(n, m, grid, (0, 0))

    # this is my attempt to solve:
    # https://practice.geeksforgeeks.org/problems/combination-sum-iii/1?page=1&category[]=Backtracking&sortBy=accuracy
    # let's start with some inner methods
    def choose_k_from_set(self, nums: list[int], k: int):
        if k > len(nums):
            return []
        if k == len(nums):
            return [nums]
        if k == 1:
            return [[n] for n in nums]

        res = []
        # there are 2 possible cases, either we add the current element, or not
        # add the current element

        temp = self.choose_k_from_set(nums[1:], k - 1)
        for i in range(len(temp)):
            temp[i] = [nums[0]] + temp[i]
        res.extend(temp)

        if len(nums) >= k + 1:
            temp = self.choose_k_from_set(nums[1:], k)
            res.extend(temp)

        return res

    def combinationSum(self, k, target):
        temp = self.choose_k_from_set(nums=list(range(1, 10)), k=k)
        return [t for t in temp if sum(t) == target]

    def permute_str(self, string: str, k: int):
        if len(string) == 0 or k == 1:
            return string

        n = len(string)
        fac_n = factorial(n)
        k = k % fac_n
        k = fac_n if k == 0 else k
        fac_n1 = fac_n // n
        rotation_factor = int(ceil(k / fac_n1)) - 1
        new_str = string[:rotation_factor] + string[rotation_factor + 1:]
        result = string[rotation_factor] + self.permute_str(new_str, k % fac_n1)
        return result

    def kthPermutation(self, n: int, k: int) -> str:
        string = ''.join([str(i) for i in range(1, n + 1)])
        return self.permute_str(string, k)

    # the next problem is:
    # https://practice.geeksforgeeks.org/problems/permutations-of-a-given-string2041/1?page=1&category[]=Backtracking&sortBy=submissions
    def inner_find_permutation(self, s):
        # let's start with some base cases:
        if len(s) <= 1:
            return [s]
        if len(s) == 2:
            return list({s[0] + s[1], s[1] + s[0]})

        res = []
        for i in range(len(s)):
            new_str = s[:i] + (s[i + 1:] if i + 1 < len(s) else '')
            temp = self.inner_find_permutation(new_str)
            # add the i-th character to the beginning of each string in the temp list
            for j in range(len(temp)):
                temp[j] = s[i] + temp[j]
            res.extend(temp)
        return res

    def find_permutation(self, s):
        return sorted(list(set(self.inner_find_permutation(s))))

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
                temp = self.InnerCombs(nums[1:], new_target)
                if len(temp) > 0:
                    for j in range(len(temp)):
                        temp[j] = current_list + temp[j]
                    res.extend(temp)
        return res

    def combinationalSum(self, nums, target):
        nums = sorted(list(set(nums)))
        if len(nums) == 0:
            return []

        res = self.InnerCombs(nums, target)
        return sorted(res, key=lambda x: tuple(x))

    def combination_of_sets(self, sets):
        # sets is a list of lists
        if len(sets) == 1:
            return sets[0]
        res = []
        sub_combination = self.combination_of_sets(sets[1:])
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
        sets = [self.phone[v] for v in a]
        return self.combination_of_sets(sets)


if __name__ == '__main__':
    sol = Solution()
    sets = [['1', '2', '3'], ['4', '5', '6']]
    r = sol.combination_of_sets(sets)
    print(r)
