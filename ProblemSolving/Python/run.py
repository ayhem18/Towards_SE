from typing import List
from graphs import neetcode as nc


def print_2d_array(a: List[List]):
    for row in a:
        r = [str(e) for e in row]
        print(" ".join(r))
    

if __name__ == '__main__':
    board = [["O","X","X","X", "X"],
             ["X","O","X","O", "O"],
             ["X","O","O","X", "X"],
             ["X","X","X","O", "X"],
             ["X","X","X","X", "X"],
             ]
    nc.solve(board)
    print_2d_array(board)
