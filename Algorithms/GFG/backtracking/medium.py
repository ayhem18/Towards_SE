# noinspection PyPep8Naming,PyShadowingNames,PyMethodMayBeStatic
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

    def find_partition(self, sets: list[list[int]], objective_set: set, current_set=None) -> bool:
        # given a list of sets, find out whether there is a partition that leads to the objective_set
        if current_set is None:
            current_set = set()

        if current_set == objective_set:
            return True

        if len(sets) == 0:
            return False

        # we are going to call the find_portion without the first element regardless
        temp = self.find_partition(sets[1:], objective_set, current_set)
        if len(current_set.intersection(sets[0])) != 0:
            return temp

        # on the other hand, if the first set does not have elements in common, then:
        current_set.update(sets[0])
        return temp or self.find_partition(sets[1:], objective_set, current_set)

    def isKPartitionPossible(self, nums, k):
        # let's group everything together
        nums = sorted(nums)
        # let's calculate the sum
        total = sum(nums)
        if total % k != 0:
            return False
        target = total // k
        # find all combinations that sum up to 'target'
        combinations = self.combination_sum(nums, target)
        # objective_set =
        pass

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
                and (y + 1, x) not in visited_pos\
                and grid[y + 1][x] == 1:
            # add the current position
            next_pos.append((y + 1, x))
            # don't forget about the mapper
            position_move_mapper[(y + 1, x)] = self.DOWN

        if x > 0 \
                and (y, x - 1) not in visited_pos\
                and grid[y][x - 1] == 1:
            next_pos.append((y, x - 1))
            position_move_mapper[(y, x - 1)] = self.LEFT

        if x + 1 < len(grid[0]) \
                and (y, x + 1) not in visited_pos\
                and grid[y][x + 1] == 1:
            next_pos.append((y, x + 1))
            position_move_mapper[(y, x + 1)] = self.RIGHT

        if y > 0 \
                and (y - 1, x) not in visited_pos\
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


if __name__ == '__main__':
    sol = Solution()
    grid = [[1, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 1, 1]]
    print(sol.findPath(grid, len(grid)))
