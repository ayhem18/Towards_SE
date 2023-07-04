"""
This script contains my solutions for the binary search section in the NeetCode road map for LeetCode problems
https://neetcode.io/roadmap
"""

# let's start with basic binary search implementation
from _collections_abc import Sequence
from math import ceil


def __binary_search(a: Sequence[int], x: int, low: int, high: int):
    if low > high:
        return -1

    mid = (low + high) // 2

    if a[mid] == x:
        return mid

    if a[mid] < x:
        return __binary_search(a, x, mid + 1, high)

    return __binary_search(a, x, low, mid - 1)


def binary_search(a: Sequence[int], x: int) -> int:
    return __binary_search(a, x, 0, len(a) - 1)


# noinspection PyMethodMayBeStatic
class Solution:
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


if __name__ == '__main__':
    s = Solution()
    piles = [30, 11, 23, 4, 20]
    h = 5
    print(s.minEatingSpeed(piles, h))
