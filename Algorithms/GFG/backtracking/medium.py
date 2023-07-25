# noinspection PyPep8Naming,PyShadowingNames,PyMethodMayBeStatic
from itertools import chain
import numpy as np


# noinspection PyMethodMayBeStatic,PyShadowingNames
class Solution:
    # let's star with a function that determines all combinations that sum up to target value
    def combination_sum(self, nums, target: int):
        # this function assumes the input is sorted
        if target < nums[0]:
            return []
        # the next base case: a list of length 1
        if len(nums) == 1:
            # since an element can be picked at most once
            return [[target]] if target == nums[0] else []
        n = nums[0]
        res = []

        for i in range(2):
            new_target = target - i * n
            current_list = [n for _ in range(i)]
            if new_target == 0:
                res.append(current_list)
            elif new_target > 0:
                temp = self.combination_sum(nums[1:], new_target)
                if len(temp) > 0:
                    for j in range(len(temp)):
                        temp[j] = current_list + temp[j]
                    res.extend(temp)
        return res

    # https://practice.geeksforgeeks.org/problems/word-search/1?page=1&category[]=Backtracking&sortBy=submissions
    # As they say 3rd time is the charm!!!
    def find_word(self, grid, current_pos, objective_str: str, visited_pos: set = None):
        if visited_pos is None:
            visited_pos = set()
        # the first base case is:
        if len(objective_str) == 0:
            return True
        y, x = current_pos
        if grid[y][x] != objective_str[0]:
            return False
        # at this point the letter at the current position is the same as the first letter
        # of the objective string which is of length 1: so basically a letter
        if len(objective_str) == 1:
            return True

        # at this point we need to add the current position to the visited_position
        visited_pos.add(current_pos)
        next_pos = []
        # detect the next positions
        if y + 1 < len(grid) and (y + 1, x) not in visited_pos:
            next_pos.append((y + 1, x))

        if x + 1 < len(grid[0]) and (y, x + 1) not in visited_pos:
            next_pos.append((y, x + 1))

        if y > 0 and (y - 1, x) not in visited_pos:
            next_pos.append((y - 1, x))

        if x > 0 and (y, x - 1) not in visited_pos:
            next_pos.append((y, x - 1))

        for pos in next_pos:
            temp = self.find_word(grid, pos, objective_str[1:], visited_pos=visited_pos)
            if temp:
                return True
        # at this point none of the options lead to the word so return False
        # after removing the current position from the visited positions
        visited_pos.discard(current_pos)
        return False

    def isWordExist(self, board, word):
        for y in range(len(board)):
            for x in range(len(board[0])):
                t = self.find_word(board, (y, x), objective_str=word)
                if t:
                    return True
        # let's get this shit started my man !!
        return False

    # let's go with rates this time:
    # https://practice.geeksforgeeks.org/problems/rat-in-a-maze-problem/1?page=1&category[]=Backtracking&sortBy=submissions
    # need some class variables for directions
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def inner_find_path(self, grid, current_pos, last_move: tuple = None, visited_pos: set = None):
        # start with default values of arguments
        if visited_pos is None:
            visited_pos = set()

        # 1st base case: where the final cell is simply inaccessible
        if grid[len(grid) - 1][len(grid[0]) - 1] == 0:
            return []

        y, x = current_pos
        if y == len(grid) - 1 and x == len(grid[0]) - 1:
            if last_move is not None:
                return [last_move]
            # this point of the code is only reached
            # when the grid is one by one (should be probably be handled in the function that calls this function)
            return []

        # time to add the current position to the visited ones
        visited_pos.add(current_pos)
        # time to consider the next positions
        next_pos = []
        position_move_mapper = {}
        if y + 1 < len(grid) \
                and (y + 1, x) not in visited_pos \
                and grid[y + 1][x] == 1:
            # add the current position
            next_pos.append((y + 1, x))
            # don't forget about the mapper
            position_move_mapper[(y + 1, x)] = self.DOWN

        if x > 0 \
                and (y, x - 1) not in visited_pos \
                and grid[y][x - 1] == 1:
            next_pos.append((y, x - 1))
            position_move_mapper[(y, x - 1)] = self.LEFT

        if x + 1 < len(grid[0]) \
                and (y, x + 1) not in visited_pos \
                and grid[y][x + 1] == 1:
            next_pos.append((y, x + 1))
            position_move_mapper[(y, x + 1)] = self.RIGHT

        if y > 0 \
                and (y - 1, x) not in visited_pos \
                and grid[y - 1][x] == 1:
            next_pos.append((y - 1, x))
            position_move_mapper[(y - 1, x)] = self.UP

        res = []
        for pos in next_pos:
            temp = self.inner_find_path(grid,
                                        pos,
                                        last_move=position_move_mapper[pos],
                                        visited_pos=visited_pos)
            if last_move is not None:
                for i in range(len(temp)):
                    temp[i] = last_move + temp[i]

            res.extend(temp)

        # at this point the algorithm is backtracking from the current_pos,
        # so it should be removed from visited positions
        visited_pos.discard(current_pos)
        return res

    def findPath(self, matrix, _: int):
        if len(matrix) == 1 and len(matrix[0]) == 1:
            return []
        if matrix[0][0] == 0:
            return []
        res = self.inner_find_path(matrix, (0, 0))
        return sorted(res)

    # time to solve some sodoku problem:
    # https://practice.geeksforgeeks.org/problems/solve-the-sudoku-1587115621/1?page=1&category[]=Backtracking&sortBy=submissions

    # first need a function to return the values present in the row of a given position
    def row_values(self, grid, position: tuple):
        y, _ = position
        res = [v for v in grid[y] if v != 0]
        return res

    def column_values(self, grid, position: tuple):
        _, x = position
        res = [grid[i][x] for i in range(len(grid)) if grid[i][x] != 0]
        return res

    def sub_square_values(self, grid, position: tuple):
        y, x = position
        yl = y // 3
        xl = x // 3
        square = np.asarray(grid)[3 * yl: 3 * (yl + 1), 3 * xl: 3 * (xl + 1)]
        square = square.tolist()
        square = list(chain(*square))
        res = [v for v in square if v != 0]
        return res

    def candidates(self, grid, pos) -> set:
        assert grid[pos[0]][pos[1]] == 0, "MAKE SURE TO CONSIDER ONLY BLANK CELLS"
        row, col, square = self.row_values(grid, pos), self.column_values(grid, pos), self.sub_square_values(grid, pos)
        # first make sure the values are unique for each domain
        if len(row) != len(set(row)) or len(col) != len(set(col)) or len(square) != len(set(square)):
            return set()

        all_values = set(row).union(set(col)).union(set(square))
        res = set(list(range(1, 10))).difference(all_values)
        return res

    def solution(self, grid, blank_positions: set):
        if len(blank_positions) == 0:
            return grid

        # iterate through the blank positions
        # and carry on with the position with the minimum number of candidates
        min_count = None
        best_pos = None
        cds = None
        for pos in blank_positions:
            # count the number of candidates
            candidates = self.candidates(grid, pos)
            # if len(candidates) == 0:
            #     return False
            if min_count is None or 0 < len(candidates) < min_count:
                min_count = len(candidates)
                best_pos = pos
                cds = candidates
        # at this point, we are choosing to fill a point with a minimum number of candidates

        for value in cds:
            y, x = best_pos
            grid[y][x] = value
            # this cell is officially no longer blank
            blank_positions.discard(best_pos)
            temp = self.solution(grid, blank_positions)
            if not isinstance(temp, bool):
                return temp

        # at this point we have tried all the possible combinations,
        return False

    def SolveSudoku(self, grid):
        # find blank positions
        blanks = [(y, x) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == 0]
        blanks = set(blanks)
        res = self.solution(grid, blanks)
        return True if not isinstance(res, bool) else False

    def printGrid(self, grid):
        # flatten the array
        flatten_array = list(chain(*grid))
        print(" ".join([str(v) for v in flatten_array]))

    def printGridBetter(self, grid):
        for row in grid:
            print(row)


if __name__ == '__main__':
    sol = Solution()
    g = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
         [5, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 7, 0, 0, 0, 0, 3, 1],
         [0, 0, 3, 0, 1, 0, 0, 8, 0],
         [9, 0, 0, 8, 6, 3, 0, 0, 5],
         [0, 5, 0, 0, 9, 0, 6, 0, 0],
         [1, 3, 0, 0, 0, 0, 2, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 7, 4],
         [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    new_g = sol.SolveSudoku(g)
    print(new_g)
    # sol.printGridBetter(new_g)
