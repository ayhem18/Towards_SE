from collections import Counter


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


if __name__ == '__main__':
    sol = Solution()
    string = 'aabbaa'
    r = sol.partition(string)
    print(r)
