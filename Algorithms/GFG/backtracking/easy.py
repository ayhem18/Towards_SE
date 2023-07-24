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

    def combinationSum(self, K, target):
        # Code here

