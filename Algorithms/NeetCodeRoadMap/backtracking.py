from collections import Counter
from itertools import chain
from copy import copy
from typing import List


# noinspection PyMethodMayBeStatic,PyShadowingNames
class Solution:
    def InnerCombs(self, nums, target: int, max_occ: dict[int, int]):
        # this function assumes the input is sorted
        if target < nums[0]:
            return []
        # the next base case
        if len(nums) == 1:
            if target % nums[0] == 0 and target // nums[0] <= max_occ[nums[0]]:
                return [[nums[0] for _ in range(target // nums[0])]]
            return []

        min_num = nums[0]
        res = []

        for i in range(max_occ[nums[0]] + 1):
            new_target = target - min_num * i
            current_list = [min_num for _ in range(i)]
            if new_target == 0:
                res.append(current_list)
            elif new_target > 0:
                temp = self.InnerCombs(nums[1:], new_target, max_occ)
                if len(temp) > 0:
                    for j in range(len(temp)):
                        temp[j] = current_list + temp[j]
                    res.extend(temp)
        return res

    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        nums = sorted(list(set(candidates)))
        # create a dictionary
        max_occ = Counter(candidates)
        res = self.InnerCombs(nums, target, max_occ)
        return res

    # for this problem:
    # https://leetcode.com/problems/permutations/description/
    def permute(self, nums: list[int]) -> list[list[int]]:
        # let's start with some base cases:
        if len(nums) <= 1:
            return [nums]
        if len(nums) == 2:
            return [[nums[0], nums[1]], [nums[1], nums[0]]]

        res = []
        for i in range(len(nums)):
            new_nums = nums[:i] + (nums[i + 1:] if i + 1 < len(nums) else [])
            temp = self.permute(new_nums)
            # add the i-th character to the beginning of each string in the temp list
            for j in range(len(temp)):
                temp[j] = [nums[i]] + temp[j]
            res.extend(temp)
        return res

    def is_palindrome(self, s: str):
        return s == s[::-1]

    # https://leetcode.com/problems/palindrome-partitioning/
    # another medium problem for the fun of it
    def partition(self, s: str) -> list[list[str]]:
        # some base cases to get started
        if len(s) == 0:
            return []

        if len(s) == 1:
            return [[s]]

        pals = [(i, s[:i]) for i in range(1, len(s)) if self.is_palindrome(s[:i])]
        res = [[s]] if self.is_palindrome(s) else []
        for index, string in pals:
            temp = self.partition(s[index:])
            for j in range(len(temp)):
                temp[j] = [string] + temp[j]
            res.extend(temp)
        return res

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

    def new_lists(self, org_list: list[int], index: int, count: int):
        def new(c: int):
            l = copy(org_list)
            l.extend([l[index]] * (c - 1))
            return l

        return [new(i) for i in range(1, count + 1)]

    def expand_list(self, org_list: list[int], counter: dict[int, int]):
        # counter is supposed to map index to the number of times a certain value appear
        res = [org_list]
        for index, c in counter.items():
            new_res = []
            for r in res:
                new_res.extend(self.new_lists(r, index, c))
            res = new_res
        return res

    def KSubsetsWithDups(self, nums: list[int], k: int, counter: Counter) -> list[list[int]]:
        if k == 0:
            return [[]]
        # the function assume nums to have distinct element
        res = []
        for index, v in enumerate(nums[:len(nums) - k + 1]):
            # first let's extract the original list of all possible list with 'k - 1' distinct elements
            k_unique = self.kSubsets(nums[index + 1:], k - 1)
            # add the value at the beginning of each list
            for i in range(len(k_unique)):
                k_unique[i] = [v] + k_unique[i]
            # now time to expand the list as needed
            # build the counter
            for l in k_unique:
                index_counter = dict([(i, counter[value]) for i, value in enumerate(l)])
                res.extend(self.expand_list(l, index_counter))
        return res

    def subsetsWithDup(self, numbers: List[int]) -> List[List[int]]:
        # first step is to convert the input to distinct elements
        nums = list(set(numbers))
        counter = Counter(numbers)
        res = [self.KSubsetsWithDups(nums, i, counter) for i in range(len(nums) + 1)]
        res = list(chain(*res))
        return res


if __name__ == '__main__':
    sol = Solution()
    nums = [1, 2, 2, 2, 2, 1]
    n = [1, 2]
    counter = Counter(nums)
    r = sol.KSubsetsWithDups(n, 0, counter)
    print(r)
