"""
The 1st script reached around 600 lines. Time for a 2nd script
"""

from typing import List
from heapq import heapify, heappush, heappop
from collections import OrderedDict, deque


# noinspection PyMethodMayBeStatic,PyShadowingNames,PyPep8Naming
class Solution:
    # starting with an easy one:
    # https://leetcode.com/problems/search-insert-position/
    def search_index(self, nums: List[int], target: int, low: int, high: int):
        # let's start with the particular case of one-element
        if len(nums) == 1:
            return 1 if target > nums[0] else 0

        if target > nums[high]:
            return high + 1
        if target < nums[low]:
            return low

        mid = (low + high) // 2

        if nums[mid] == target:
            return mid

        if nums[mid] > target > nums[mid - 1]:
            return mid
        if nums[mid + 1] > target > nums[mid]:
            return mid + 1

        if nums[mid] > target:
            return self.search_index(nums, target, low, mid - 1)

        return self.search_index(nums, target, mid + 1, high)

    def searchInsert(self, nums: List[int], target: int) -> int:
        return self.search_index(nums, target, 0, len(nums) - 1)

    # let's define a special tuple for our problem here
    class SlideTuple:
        def __init__(self, index: int, value: int, k: int):
            self.index = index
            self.value = value
            self.k = k

        def __lt__(self, nxt):
            return self.value < nxt.yos

    class SlideTuple:
        def __init__(self, index: int, val: int):
            self.index = index
            self.val = val

        def __lt__(self, other):
            return self.val < other.val or self.val == other.val and self.index < other.index

        def __eq__(self, other):
            return self.val == other.val and self.index == other.index

        def __gt__(self, other):
            return self.val > other.val or (self.val == other.val and self.index > other.index)

        def __getitem__(self, item):
            return self.index if item == 0 else self.val

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:

        heap = [self.SlideTuple(index, -v) for index, v in enumerate(nums[:k])]
        heapify(heap)
        save = OrderedDict()

        def find_max_element(i):
            while True:
                index, val = heap[0][0], -heap[0][1]
                if i + k - 1 >= index >= i:
                    return index, val
                else:
                    # remove the element
                    heappop(heap)

        for i in range(0, len(nums) - k):
            # find the maximum element
            max_index, max_element = find_max_element(i)
            save[i] = max_element
            # only pop the element if it is the maximum number
            if max_index == i and max_element == nums[i]:
                heappop(heap)
            heappush(heap, self.SlideTuple(i + k, -nums[i + k]))

        save[len(nums) - k] = find_max_element(len(nums) - k)[1]
        return [v for k, v in save.items()]

    # a problem listed as medium for some reason...
    # well it is definitely annoying...
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        C, R = len(matrix[0]), len(matrix)
        if C == 1:
            return [row[0] for row in matrix]

        if R == 1:
            return matrix[0]

        lower_row, upper_row = 0, R - 1
        lower_col, upper_col = 0, C - 1
        res = []
        count = 0

        while lower_row <= upper_row and lower_col <= upper_col:
            if count < R * C:
                for i in range(lower_col, upper_col + 1):
                    res.append(matrix[lower_row][i])
                    count += 1

            lower_row += 1
            if count < R * C:
                for j in range(lower_row, upper_row + 1):
                    res.append(matrix[j][upper_col])
                    count += 1

            upper_col -= 1
            if count < R * C:
                for i in range(upper_col, lower_col - 1, -1):
                    res.append(matrix[upper_row][i])
                    count += 1

            upper_row -= 1
            if count < R * C:
                for j in range(upper_row, lower_row - 1, -1):
                    res.append(matrix[j][lower_col])
                    count += 1

            lower_col += 1

        return res

    def lengthOfLIS(self, nums: List[int]) -> int:
        # my solution is DP, and quadratic in time
        # apparently there is a O(nlog(n)) solution
        # but let's make this work for the moment
        values = [0 for _ in nums]

        if len(nums) == 1:
            return 1

        values[1] = 1 + int(nums[-2] < nums[-1])
        max_value = values[1]
        for i in range(len(nums) - 3, -1, -1):
            # each iteration will set values[len(nums) - 1 - i] which corresponds to length of LTS
            # starting from i
            j1 = None
            for j in range(i + 1, len(nums)):
                if nums[j] > nums[i]:
                    j1 = j
                    break

            if j1 is None:
                values[len(nums) - 1 - i] = 1
                continue
            candidates = [j1]
            candidates.extend([c for c in range(j1, len(nums)) if nums[j1] > nums[c] > nums[i]])

            values[len(nums) - 1 - i] = 1 + max([values[len(nums) - 1 - c] for c in candidates])

            max_value = max(max_value, values[len(nums) - 1 - i])

        return max_value

    # def increasingPathScore(self,
    #                         matrix: List[List[int]],
    #                         y: int,
    #                         x: int,
    #                         values: List[List[int]] = None) -> int:
    #     rows = len(matrix)
    #     cols = len(matrix[0])
    #
    #     if values is None:
    #         values = [[0 for _ in range(cols)] for _ in range(rows)]
    #
    #     if values[y][x] != 0:
    #         # it means this cell has already been considered
    #         return values[y][x]
    #
    #     # at this point set it to 1, cause any cell has at least a score of '1'
    #     values[y][x] = 1
    #
    #     next_cells = [(t[0], t[1]) for t in [(y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)]
    #                   if rows > t[0] >= 0 and cols > t[1] >= 0 and matrix[t[0]][t[1]] > matrix[y][x]]
    #
    #     # sort them in descending order
    #     next_cells = sorted(next_cells, key=lambda t: matrix[t[0]][t[1]], reverse=True)
    #
    #     for (y1, x1) in next_cells:
    #         values[y][x] = max(1 + self.increasingPathScore(matrix, y1, x1, values), values[y][x])
    #
    #     return values[y][x]
    #
    # def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
    #     rows = len(matrix)
    #     cols = len(matrix[0])
    #
    #     max_value = 0
    #     for y in range(rows):
    #         for x in range(cols):
    #             v = self.increasingPathScore(matrix, y, x)
    #             max_value = max(v, max_value)
    #
    #     return max_value

    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows = len(matrix)
        cols = len(matrix[0])

        maps = {}
        vals = set()
        for r, rv in enumerate(matrix):
            for c, v in enumerate(rv):
                vals.add(v)
                if v not in maps:
                    maps[v] = set()

                maps[v].add((r, c))

        # convert to a list
        vals = sorted(list(vals), reverse=True)
        values = [[1 for _ in r] for r in matrix]

        max_score = 1
        for v in vals:
            for y, x in maps[v]:
                next_cells = [(t[0], t[1]) for t in [(y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)]
                              if rows > t[0] >= 0 and cols > t[1] >= 0 and matrix[t[0]][t[1]] > matrix[y][x]]

                # iterate through the next cells:
                # it is guaranteed that the score of any chosen cell is already computed
                for y1, x1 in next_cells:
                    values[y][x] = max(values[y][x], 1 + values[y1][x1])

                max_score = max(max_score, values[y][x])

        return max_score


# the idea here is very simplistic:
# implementing a stack with 2 queues
#: https://leetcode.com/problems/implement-stack-using-queues/submissions/
# nice the solution works !!
class MyStack:
    def __init__(self):
        # as indicated by the problem statement, the idea is to use 2  queues
        self.q1 = deque()
        self.q2 = deque()

    def push(self, x: int) -> None:
        # push to whatever queue has larger number of element
        max_q = max([self.q1, self.q2], key=len)
        # this pushes the element to the end of the queue
        max_q.append(x)

    # since pop() and top() are quite similar in functionalities, a utility function is written
    # to save the common part between them

    def pop(self) -> int:
        max_q, min_q = (self.q1, self.q2) if len(self.q1) > len(self.q2) else (self.q2, self.q1)
        # the idea is to reduce the largest queue to only contain one element:
        # that element will either be removed: pop
        # or simply put in the other queue: top
        while len(max_q) > 1:
            # max_q.popleft() corresponds to pop for a usual queue
            min_q.append(max_q.popleft())

        return max_q.popleft()

    def top(self) -> int:
        max_q, min_q = (self.q1, self.q2) if len(self.q1) > len(self.q2) else (self.q2, self.q1)
        # the idea is to reduce the largest queue to only contain one element:
        # that element will either be removed: pop
        # or simply put in the other queue: top
        while len(max_q) > 1:
            # max_q.popleft() corresponds to pop for a usual queue
            min_q.append(max_q.popleft())
        # at this point  return the only element in max_q
        top = max_q[0]

        # put in min_q
        min_q.append(max_q.popleft())
        return top

    def empty(self) -> bool:
        return len(self.q1) + len(self.q2) == 0


if __name__ == '__main__':
    s = MyStack()
    l = list(range(1, 1))
    for v in l:
        s.push(v)

    new_l = []
    while not s.empty():
        new_l.append(s.pop())

    assert new_l == l[::-1]