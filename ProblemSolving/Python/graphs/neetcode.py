"""
This script contains my attempts to solve the NeetCode Problems in the Graph section
"""

from typing import List, Dict, Optional

from collections import deque

"""
Problems: 
https://leetcode.com/problems/number-of-islands/description/
and
https://leetcode.com/problems/max-area-of-island/ 

are basically solved by find the number of connected components in the graph
"""

class _Counter:
    def __init__(self, val) -> None:
        self.c = val

    def increment(self):
        self.c += 1

def _graph_dfs(adj_list: List[List[int]], start_vertex: int, visited: Dict, result: List[int], counter: _Counter) -> List[int]:
    result[counter.c] = start_vertex
    visited[start_vertex] = True
    for v in adj_list[start_vertex]:
        if not visited[v]:
            counter.increment()
            _graph_dfs(adj_list, start_vertex=v, visited=visited, result=result, counter=counter)    

def graph_dfs(adj_list: List[List[int]], 
              start_vertex: int, 
              visited:Dict=None) -> List[int]:
    
    res = [None for _ in range(len(adj_list))]
    # modify the results thourgh dfs
    if visited is None:
        visited = dict([(v, False) for v in range(len(adj_list))])
    
    counter = _Counter(0)
    _graph_dfs(adj_list, start_vertex=start_vertex, visited=visited, result=res, counter=counter)
    # make sure to trim the result
    res = [v for v in res if v is not None]
    return res

def graph_connected_components(adj_list: List[List[int]]) -> List[List]:
    
    n_vertices = len(adj_list)
    count_vis = 0
    
    # create the visited dict
    visited = dict([(v, False) for v in range(len(adj_list))])

    start_vertex = 0

    max_area = 0
    components = []
    
    while count_vis < n_vertices:
        while start_vertex < n_vertices and visited[start_vertex]:
            start_vertex += 1

        # this means we visited all vertices
        if start_vertex == n_vertices:
            break

        component_vertices = graph_dfs(adj_list=adj_list, start_vertex=start_vertex, visited=visited)
        max_area = max(max_area, len(component_vertices))
        components.append(component_vertices)
        count_vis += len(component_vertices)        

    return max_area
    
def maxAreaOfIsland(grid: List[List[int]]) -> int:
    n1 = len(grid)
    n2 = len(grid[0])
    counter: int = 0

    coord_counter_map = {}

    for i in range(n1):
        for j in range(n2):
            if grid[i][j] == 1:
                coord_counter_map[(i, j)] = counter
                counter += 1

    if counter == 0:
        return 0

    # create an adjacency list
    adj_list = [[] for _ in range(counter)] # since a vertex can have a degree of at most 4, appending to the lists should not be an issue.

    # iterate through the grid again
    for i in range(n1):
        for j in range(n2):
            if grid[i][j] == 1:
                index = coord_counter_map[(i, j)]

                # (i - 1, j) (i + 1, j) (i, j - 1), (i, j + 1)

                if j > 0 and grid[i][j - 1] == 1:
                    adj_list[index].append(coord_counter_map[(i, j - 1)])

                if j + 1 < n2 and grid[i][j + 1] == 1:
                    adj_list[index].append(coord_counter_map[(i, j + 1)])

                if i > 0 and grid[i - 1][j] == 1:
                    adj_list[index].append(coord_counter_map[(i - 1, j)])

                if i + 1 < n1 and grid[i + 1][j] == 1:
                    adj_list[index].append(coord_counter_map[(i + 1, j)])

    # now the adjacency list is ready
    return graph_connected_components(adj_list=adj_list)
        

"""
https://leetcode.com/problems/clone-graph/
"""

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def cloneGraph(node: Optional['Node']) -> Optional['Node']:
    # first find the number of nodes 
    visited_nodes = set()
    max_val = 0
    
    queue = deque(node)

    while len(queue) != 0:
        current_node = queue[0]
        
        visited_nodes.add(current_node.val)
        
        for n in current_node.neighbors:
            if n.val not in visited_nodes:
                queue.append(n)
                visited_nodes.add(n.val)
                max_val = max(max_val, n.val)
        queue.popleft()

    # build an adjacency list
    

if __name__ == '__main__':
    pass
