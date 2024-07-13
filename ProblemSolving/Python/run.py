from typing import List
from graphs import neetcode as nc


def print_2d_array(a: List[List]):
    for row in a:
        r = [str(e) for e in row]
        print(" ".join(r))
    

if __name__ == '__main__':
    edges = [[1,2],[2, 3], [1,3]]
    print(nc.findRedundantConnection(edges))
