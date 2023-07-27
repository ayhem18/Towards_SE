from collections import Counter
from itertools import chain
from copy import deepcopy
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

    # the functions below solve the 2 subsets challenges:
    # https://leetcode.com/problems/subsets/
    # https://leetcode.com/problems/subsets-ii/

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
            l = deepcopy(org_list)
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

    # the last problem in the backtracking problem set
    # let's set some constants to work with
    EMPTY = 0
    ATTACKED = -1

    def queen_range(self, grid: list[list[int]], pos: tuple[int, int], value_set):
        # let's extract position
        y, x = pos
        seen_pos = set()

        # set the column
        for i in range(len(grid)):
            if (i, x) not in seen_pos:
                grid[i][x] += value_set
                seen_pos.add((i, x))

        # set the row
        for i in range(len(grid[0])):
            if (y, i) not in seen_pos:
                grid[y][i] += value_set
                seen_pos.add((y, i))

        yt, xt = y, x
        # set the diagonal left + up
        while yt > -1 and xt < len(grid[0]):
            if (yt, xt) not in seen_pos:
                grid[yt][xt] += value_set
                seen_pos.add((yt, xt))

            # increase xt
            xt += 1
            # decrease yt
            yt -= 1

        yt, xt = y, x
        # set the diagonal left + up
        while yt > -1 and xt > -1:
            if (yt, xt) not in seen_pos:
                grid[yt][xt] += value_set
                seen_pos.add((yt, xt))

            # increase xt
            xt -= 1
            # decrease yt
            yt -= 1

        yt, xt = y, x
        # set the diagonal right
        while yt < len(grid) and xt > -1:
            if (yt, xt) not in seen_pos:
                grid[yt][xt] += value_set
                seen_pos.add((yt, xt))

            # increase xt
            xt -= 1
            # decrease yt
            yt += 1

        yt, xt = y, x
        # set the diagonal right
        while yt < len(grid) and xt < len(grid[0]):
            if (yt, xt) not in seen_pos:
                grid[yt][xt] += value_set
                seen_pos.add((yt, xt))

            # increase xt
            xt += 1
            # decrease yt
            yt += 1
        pass

    def nQueens(self, grid: list[list[int]], n: int):
        # let's start with a base case:
        if n == len(grid):
            return [[]]
        # now the idea is to check the values at the n-th row
        empty_pos = [(n, x) for x in range(len(grid[0])) if grid[n][x] == self.EMPTY]

        res = []

        for pos in empty_pos:
            # first attack
            self.queen_range(grid, pos, -1)
            # proceed with the next row
            next_row = self.nQueens(grid, n + 1)
            for i in range(len(next_row)):
                next_row[i] = [pos] + next_row[i]
            res.extend(next_row)
            # make sure to clear the cells attacked by the current position
            self.queen_range(grid, pos, 1)

        return res

    def solveNQueens(self, n: int) -> List[List[str]]:
        # create an empty grid
        grid = [[self.EMPTY for _ in range(n)] for _ in range(n)]
        combs = self.nQueens(grid, 0)
        output = []

        for combination in combs:
            grid_copy = deepcopy(grid)
            for p in combination:
                grid_copy[p[0]][p[1]] = self.ATTACKED
            output.append(self.to_output(grid_copy))
            # output.append(grid_copy)
        # convert the grid now to the desired output
        return output

    def to_output(self, grid):
        g = ["".join(['.' if v == self.EMPTY else 'Q' for v in row]) for row in grid]
        return g


def print_grid(g):
    for r in g:
        print(r)


if __name__ == '__main__':
    sol = Solution()
    n = 4
    r = sol.solveNQueens(n)
    for g in r:
        print_grid(g)
        print("#" * 10)