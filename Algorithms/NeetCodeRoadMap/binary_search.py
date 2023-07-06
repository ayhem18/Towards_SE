"""
This script contains my solutions for the binary search section in the NeetCode road map for LeetCode problems
https://neetcode.io/roadmap
"""
import random
# let's start with basic binary search implementation
from _collections_abc import Sequence
from math import ceil

random.seed(60)


# noinspection PyMethodMayBeStatic
class Solution:
    def __binary_search(self, a: Sequence[int], x: int, low: int, high: int):
        if low > high:
            return -1

        mid = (low + high) // 2

        if a[mid] == x:
            return mid

        if a[mid] < x:
            return self.__binary_search(a, x, mid + 1, high)

        return self.__binary_search(a, x, low, mid - 1)

    def binary_search(self, a: Sequence[int], x: int) -> int:
        return self.__binary_search(a, x, 0, len(a) - 1)

    def __pair_to_int(self, pair: tuple[int, int], columns: int):
        c1, c2 = pair
        return c1 * columns + c2

    def __int_to_pair(self, n: int, columns: int):
        return n // columns, n % columns

    def __search_matrix(self, matrix: list[list[int]], target: int, low: int, high: int) -> bool:
        columns = len(matrix[0])

        if low > high:
            return False

        mid = int((low + high) / 2)

        mid_pair = self.__int_to_pair(mid, columns)

        v = matrix[mid_pair[0]][mid_pair[1]]

        if v == target:
            return True

        if v > target:
            return self.__search_matrix(matrix, target, low, mid - 1)

        return self.__search_matrix(matrix, target, mid + 1, high)

    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        rows = len(matrix)
        columns = len(matrix[0])
        return self.__search_matrix(matrix, target, 0, self.__pair_to_int((rows - 1, columns - 1), columns))

    def __score(self, piles: list[int], rate: int):
        return sum([int(ceil(p / rate)) for p in piles])

    def __eat_speed(self, piles: list[int], h: int, low: int, high: int):
        while high - low > 1:
            # first calculate mid
            mid = int((low + high) / 2)
            score = self.__score(piles, mid)
            if score > h:
                low = mid
            else:
                high = mid

        return high

    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        # let's first calculate the minimum rate
        min_pile, max_pile = min(piles), max(piles)
        min_rate = int(min_pile / int(ceil(h / len(piles))))
        max_rate = int(ceil(max_pile / int(h / len(piles))))
        return self.__eat_speed(piles, h, low=min_rate, high=max_rate)

    def min_rotated_sorted(self, a: list[int], low: int, high: int):
        if high - low <= 2:
            return min(a[low: high + 1])

        mid = int((low + high) / 2)

        if a[low] > a[mid]:
            return self.min_rotated_sorted(a, low + 1, mid)

        if a[mid] > a[high]:
            return self.min_rotated_sorted(a, mid + 1, high)

        # this point we have a[low] <= a[mid] <= a[high]
        if a[high] > a[mid]:
            # At this point,  we can't have min in the interval [mid + 1, high]
            return self.min_rotated_sorted(a, low, mid)

        # at this point we have: a[high] == a[mid] >= a[low]
        # if the minimum value (lower than a[high]) is indeed in the interval [mid + 1, high - 1]
        # that means the interval [low, mid] is full of the same value
        # the scenario than the min value is located in interval (low, mid) is more likely
        temp_res = self.min_rotated_sorted(a, low, mid)
        if temp_res < a[mid]:
            return temp_res

        return self.min_rotated_sorted(a, mid + 1, high - 1)

    def findMin(self, nums: list[int]) -> int:
        # find the minimum element in a rotated sorted array
        return self.min_rotated_sorted(nums, 0, len(nums) - 1)

    def search_rotated_array(self, a: list[int], target: int, low: int, high: int):
        # first the task is reduced  to ordinary binary search
        if a[low] < a[high]:
            return self.__binary_search(a, target, low, high)

        # base case: if low > high
        if low >= high:
            return -1

        # we have a[low] > a[high] (under the assumption that all elements are distinct
        # define mid
        mid = int((low + high) / 2)
        if target == a[mid]:
            return mid

        if a[mid] > a[high]:
            # the min point is in the interval [mid + 1, high]
            if target > a[mid] or target <= a[high]:
                return self.search_rotated_array(a, target, mid + 1, high)

            return self.search_rotated_array(a, target, low, mid - 1)

        if a[mid] < a[high]:
            # the min point is in the interval [low, mid]
            if target >= a[low] or target < a[mid]:
                return self.search_rotated_array(a, target, low, mid - 1)

            return self.search_rotated_array(a, target, mid + 1, high)

        # if the code reaches this point, it means
        # that mid == high:
        return self.search_rotated_array(a, target, low, mid - 1)

    def search(self, nums: list[int], target: int) -> int:
        return self.search_rotated_array(nums, target, 0, len(nums) - 1)


def rotate(sorted_array: list[int], n: int):
    new_array = sorted_array.copy()
    for i, v in enumerate(sorted_array):
        new_array[(i + n) % len(new_array)] = v
    return new_array


if __name__ == '__main__':
    s = Solution()
    a = [3, 1]
    s.search(a, -1)

    # a = [1, 2, 3, 4, 5, 6, 20, 50, 70, 71, 81, 89, 90, 100, 120]
    #
    # for i in range(len(a)):
    #     new_a = rotate(a, i)
    #     for _ in range(10):
    #         target = random.randint(1, 120)
    #
    #         index = s.search(new_a, target)
    #         if index == -1:
    #             assert target not in new_a
    #         else:
    #             assert new_a[index] == target
