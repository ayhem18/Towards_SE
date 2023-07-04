"""
This scripts contains my solutions for the leet code problems
mentioned in the 2 pointers section of the NeetCode roadmap
"""

from math import ceil
from collections import deque


def binary_search_inner(array: list, x, low, high):
    while low <= high:

        mid = low + (high - low) // 2

        if array[mid] == x:
            return mid

        elif array[mid] < x:
            low = mid + 1

        else:
            high = mid - 1

    return -1


def binary_search(array, x):
    return binary_search_inner(array, x, 0, len(array) - 1)


# noinspection PyMethodMayBeStatic
class Solution:
    # well this solution is O(log(n)) which is a shame by the way
    def twoSumBS(self, numbers: list[int], target: int) -> list[int]:
        # the twick to this problem, is that I have to use only constant space,
        # so I have to use binary search
        for i in range(len(numbers)):
            if numbers[i] <= target / 2:
                index = binary_search_inner(numbers, target - numbers[i], i + 1, len(numbers) - 1)
                if index != -1:
                    return [i, index]

        return [-1, -1]

    # let's come up with a O(n) solution
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        p1, p2 = 0, len(numbers) - 1
        while p2 > p1:
            # time to decrement the upper index
            while numbers[p1] + numbers[p2] > target:
                # decrease p2 to the next value
                p2 -= 1

            if numbers[p1] + numbers[p2] == target:
                return [p1 + 1, p2 + 1]

            # now increase p1
            p1 += 1

        return [-1, -1]

    # this function finds all occurrences in a sorted array
    def two_sum(self, nums: list[int], target: int) -> list[list[int]]:
        p1, p2 = 0, len(nums) - 1
        last_p1 = nums[p1]
        res = []
        while p2 > p1:
            while p2 > 0 and nums[p1] + nums[p2] > target:
                p2 -= 1

            if p2 > p1 and nums[p1] + nums[p2] == target:
                res.append((nums[p1], nums[p2]))

            while p1 < p2 and nums[p1] == last_p1:
                p1 += 1
            last_p1 = nums[p1]

        return res

    def threeSum(self, nums: list[int], target: int = 0) -> list[list[int]]:
        assert len(nums) >= 3, "The array must be of length 3 at least"
        l = len(nums)
        nums = sorted(nums)
        upper_bound = int(ceil(target / 3))
        lower_bound = target - (nums[-1] + nums[-2])
        last = None
        res = []
        for i in range(0, l - 2):
            n = nums[i]
            if upper_bound >= n >= lower_bound and (last is None or n != last):
                temp = self.two_sum(nums[i + 1:], target - nums[i])
                res.extend([(n,) + t for t in temp])
                last = n

        return res

    def maxArea(self, a: list[int]) -> int:
        # technically given an array of integer, this function finds, i, j for maximizing:
        # min(a[i], a[j]) * |j - i|
        p1, p2 = 0, len(a) - 1
        max_area = p2 * min(a[p1], a[p2])
        while True:
            while p1 < p2 and a[p1] <= a[p2]:
                p1 += 1
            if p1 < p2:
                new_area = p2 * min(a[p1], a[p2])
                max_area = max(max_area, new_area)
            # the 2 pointers crossed each other, no more work needs to be done
            else:
                break
            # now we have a[p1] < a[p2]
            # we do the opposite: decrement p2
            while p1 < p2 and a[p1] >= a[p2]:
                p2 -= 1
            if p1 < p2:
                new_area = p2 * min(a[p1], a[p2])
                max_area = max(max_area, new_area)
            else:
                break
        return max_area

    # probably the first hard problem I attempt (not really that hard)
    def trap_slow(self, a: list[int]) -> int:
        if len(a) <= 1:
            return 0

        # find the first index of a bar with non-zero value
        p1 = 0
        while p1 < len(a) and a[p1] == 0:
            p1 += 1
        # rule the case where the entire array is zeros
        if p1 >= len(a):
            return 0

        p2 = p1 + 1
        temp = p1 + 1
        while p2 < len(a) and a[p1] > a[p2]:
            if a[p2] >= a[temp]:
                temp = p2
            p2 += 1

        # now there are 2 cases
        if p2 >= len(a):
            return sum([a[temp] - a[i] for i in range(p1 + 1, temp)]) + self.trap_slow(a[temp:])

        # 2nd case: there is a number larger than a[p1]
        first_part = sum([a[p1] - a[i] for i in range(p1 + 1, p2)])
        return first_part + self.trap_slow(a[p2:])

    # I might have stated that this problem is not that hard, but I take it back. Nevertheless,
    # it is cool to start working on stuff like that

    def water(self, points: tuple[int, int], a: list[int]):
        i1, i2 = points
        return sum([min(a[i1], a[i2]) - a[i] for i in range(i1 + 1, i2)])

    def trap(self, a: list[int]):
        # find the first non-zero bar
        i = 0
        while i < len(a) and a[i] == 0:
            i += 1

        if i >= len(a):
            return 0

        # now we define the descending stack
        desc_stack = deque()
        points = deque()
        while i < len(a):
            while i < len(a) - 1 and a[i] >= a[i + 1]:
                desc_stack.append(i)
                i += 1

            # we reached the end and the last portion was non-decreasing
            if i >= len(a) - 1:
                res = sum([self.water(p, a) for p in points])
                return res

            # at this point we have a[i + 1] > a[i]
            last_index = None
            while len(desc_stack) != 0:
                last_index = desc_stack[-1]
                if a[last_index] >= a[i + 1]:
                    break
                # remove the last index if the current value is higher
                desc_stack.pop()

            if last_index is None:
                i = i + 1
                continue

            new_point = (last_index, i + 1)
            # now time to add the new point

            while len(points) != 0 and points[-1][0] >= last_index:
                points.pop()

            # add the new point regardless
            points.append(new_point)
            i = i + 1

        # the final return is the sum of the water trapped at each of the saved points
        res = sum([self.water(p, a) for p in points])
        return res


if __name__ == '__main__':
    s = Solution()
    a = [1, 7, 5]
    print(s.trap(a))
