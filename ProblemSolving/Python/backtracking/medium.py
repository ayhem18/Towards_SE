# noinspection PyPep8Naming,PyShadowingNames,PyMethodMayBeStatic    def wordBoggle(self,board,dictionary):


import numpy as np
from typing import List, Tuple
from itertools import chain
from collections import defaultdict
from copy import deepcopy

from backtracking.standard import all_subsets


# let's star with a function that determines all combinations that sum up to target value
def combination_sum(nums, target: int):
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
            temp = combination_sum(nums[1:], new_target)
            if len(temp) > 0:
                for j in range(len(temp)):
                    temp[j] = current_list + temp[j]
                res.extend(temp)
    return res

# https://practice.geeksforgeeks.org/problems/word-search/1?page=1&category[]=Backtracking&sortBy=submissions
def find_word(grid, current_pos, objective_str: str, visited_pos: set = None):
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
        temp = find_word(grid, pos, objective_str[1:], visited_pos=visited_pos)
        if temp:
            return True
    # at this point none of the options lead to the word so return False
    # after removing the current position from the visited positions
    visited_pos.discard(current_pos)
    return False

def isWordExist(board, word):
    for y in range(len(board)):
        for x in range(len(board[0])):
            t = find_word(board, (y, x), objective_str=word)
            if t:
                return True
    return False

# https://www.geeksforgeeks.org/problems/word-boggle4143/1?page=1&category=Backtracking&status=unsolved&sortBy=submissions
def find_word_on_board(board:List[List], word: str, initial_y: int, initial_x: int, steps: List[Tuple[int]]) -> bool:
    # we assume that initial position corresponds to the first letter of the word, when this function is called
    steps.append((initial_y, initial_x))

    # set the position to -1 on the board 
    board[initial_y][initial_x] = -1

    if len(word) == 1:
        return True

    # look for in-boundry cells
    next_cells = [ (initial_y + i, initial_x + j) for i in range(-1, 2) for j in range(-1, 2) if 0 <= (i + initial_y) < len(board) and 0 <= (j + initial_x) < len(board[0])]
    # keep only the cells that contain the next letter    
    next_cells = [ (y, x) for (y, x) in next_cells if board[y][x] == word[1]]

    if len(next_cells) == 0:
        return False
    
    for y, x in next_cells:
        temp = find_word_on_board(board, word[1:], initial_x=x, initial_y=y, steps=steps)
        
        if temp:
            # the moment we find it, no need to proceed further
            return True

    # the word cannot be built from the board
    return False

def wordBoggle(board: List[List], words: set):
    # a copy of the board to be traversed
    copy_board = deepcopy(board)
    

    # iterate through the board and build a map between letters and positions
    letter_positions = defaultdict(lambda : [])

    for i in range(len(board)):
        for j in range(len(board[0])):
            letter_positions[board[i][j]].append((i, j))

    found_words = set()

    for w in words:
        if w[0] not in letter_positions:
            continue
            
        # iterate through all the possible initial positions
        for iy, ix in letter_positions[w[0]]:
            steps = []
            word_found = find_word_on_board(board=copy_board, word=w, initial_y=iy, initial_x=ix, steps=steps)

            # clear the board from the "-1" cells
            for y, x in steps:
                copy_board[y][x] = board[y][x]
            
            if word_found:
                found_words.add(w)
                break

    return sorted(list(found_words))


# probably my first time using recursion this very specific way
# https://www.geeksforgeeks.org/problems/decode-the-string2444/1?page=1&category=Backtracking&status=unsolved&sortBy=submissions
def decode_inner_string(string: str) -> Tuple[str, int]:
    str_counter = 0

    decoded_str = ""

    while string[str_counter] != "]":
        # add any letter
        if string[str_counter].isalpha():
            decoded_str += string[str_counter]
            str_counter += 1
        
        elif string[str_counter].isdigit():
            number = string[str_counter]
            digit_counter = str_counter + 1

            while string[digit_counter].isdigit():
                digit_counter += 1
                number += string[digit_counter]

            # at this point the number was formed
            # move the string counter to the digit_counter value + 1 (since we have "[" right after the digit)
            str_counter = digit_counter + 1 

            recursive_decoded_string, length = decode_inner_string(string[str_counter:])
            
            str_counter += length

            decoded_str += int(number) * recursive_decoded_string

    # add one for the "]" character
    str_counter += 1

    return decoded_str, str_counter

def decodedString(string: str) -> str:
    n = len(string)
    str_counter = 0

    decoded_str = ""


    while str_counter < n:
        
        if string[str_counter].isalpha():
            decoded_str += string[str_counter]
            str_counter += 1

        elif string[str_counter].isdigit():
            # the "number" can have multiple digits
            number = string[str_counter]
            digit_counter = str_counter + 1

            while string[digit_counter].isdigit():
                number += string[digit_counter]
                digit_counter += 1

            # at this point the number was formed
            # move the string ocunter to the digit counter value + 1 (since we have "[" right after the digit)
            str_counter = digit_counter + 1 

            inner_str, inner_str_org_length = decode_inner_string(string[str_counter:])

            str_counter += inner_str_org_length

            decoded_str += int(number) * inner_str


    return decoded_str


# https://www.geeksforgeeks.org/problems/permutation-with-spaces3627/1?page=1&category=Backtracking&status=unsolved&sortBy=submissions

# the problem first requires determining all the subsets of the list [1, length(str) - 1]
# each subset maps to a unique string
def add_spaces(string: str, space_positions: List[int]) -> str:
    if len(space_positions) == 0:
        return string 

    last_space_index = 0
    new_str = string[0]
    counter = 1
    
    for counter in range(1, len(string)):
        if last_space_index < len(space_positions) and  counter == space_positions[last_space_index]:
            new_str += " " 
            last_space_index += 1
            
        new_str += string[counter]

    return new_str

def permutation(s: str) -> List[str]:
    n = len(s)
    
    if n == 1:
        return [s]
    
    spaces_positions = all_subsets(list(range(1, n)))
    return sorted([add_spaces(s, sp) for sp in spaces_positions])

class Solution:

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

