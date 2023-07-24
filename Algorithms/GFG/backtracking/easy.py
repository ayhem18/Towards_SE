from math import factorial, ceil


# noinspection PyMethodMayBeStatic,PyShadowingNames
class Solution:
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

if __name__ == '__main__':
    sol = Solution()
    string = '1234'
    for i in range(1, 25):
        r = sol.permute_str(string, i)
        print(i, r, sep='\t')
