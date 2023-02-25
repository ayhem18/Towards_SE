class Solution:
    def binary_search(self, array: list, x, low, high):
        while low <= high:

            mid = low + (high - low) // 2

            if array[mid] == x:
                return mid

            elif array[mid] < x:
                low = mid + 1

            else:
                high = mid - 1

        return -1

    def two_sum(self, nums: list[int], target: int) -> list[int]:
        """
        Given an array of numbers, find the indices of the pair of values whose sum is equal to target
        The assumption is that such pair appears exactly once in "nums" array
        :param nums:  of values
        :param target: the
        :return:
        """
        ## The solution passed the tests!!!! GREAT

        # first sort the array of values
        sorted_nums = sorted(nums)
        length = len(nums)
        res = []
        for index, n in enumerate(nums):
            # this means the pair was found
            if self.binary_search(sorted_nums, target - n, low=index, high=length - 1) != -1:
                # there are two possibilities when entering this block of code
                # first the bad one: target / 2 is present once and the conditional above can't detect it
                # loop through the indices of the original list
                for i in range(len(nums)):
                    if nums[i] == n and len(res) == 0:
                        res.append(i)
                    elif nums[i] == target - n and i not in res:
                        res.append(i)
                        return res
                # if this part of the code is reached: it means the pair found was indeed a false alarm
                res.clear()
        return [-1, -1]

    def two_sum_2(self, nums: list[int], target: int) -> list[int]:
        # this solution beats up ~62% speed-wise, but it is in the last 6.51% percentile memory-wise
        values_indices = {}
        for index, val in enumerate(nums):
            if val not in values_indices:
                values_indices[val] = [index]
            else:
                values_indices[val].append(index)
        for n in nums:
            if target - n in values_indices:
                if target - n != n:
                    return [values_indices[n][0], values_indices[target - n][0]]
                else:
                    if len(values_indices[n]) > 1:
                        return [values_indices[n][0], values_indices[n][1]]

        return [-1, -1]


def main():
    sol = Solution()
    nums = [3, 3]
    t = 6
    print(sol.two_sum(nums, t))


if __name__ == "__main__":
    main()
