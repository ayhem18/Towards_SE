"""
This script contains my attempts to solve the NeetCode Problems in the Graph section
"""

from typing import List, Optional
from collections import deque

from .common import graph_dfs, graph_connected_components, _graph_bfs, edgesList2adjList, is_graph_connected

"""
Problems: 
https://leetcode.com/problems/number-of-islands/description/
and
https://leetcode.com/problems/max-area-of-island/ 

are basically solved by find the number of connected components in the graph
"""

def _graph_connected_components(adj_list: List[List[int]]) -> List[List]:
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
    return _graph_connected_components(adj_list=adj_list)
        

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
    

"""
https://leetcode.com/problems/rotting-oranges/
"""
def orangesRotting(grid: List[List[int]]) -> int:
    n1 = len(grid)
    n2 = len(grid[0])
    counter: int = 0

    coord_counter_map = {}
    rotten_indices = []
    for i in range(n1):
        for j in range(n2):
            if grid[i][j] in [1, 2]:
                coord_counter_map[(i, j)] = counter
                if grid[i][j] == 2:
                    rotten_indices.append(counter)
                counter += 1

    # if there are no fresh oranges (or no oranges at all), return 0
    if len(coord_counter_map) == len(rotten_indices) or counter == 0:
        return 0
    
    # if there are no rotten oranges return -1
    if len(rotten_indices) == 0:
        return -1

    # create an adjacency list
    adj_list = [[] for _ in range(counter)] # since a vertex can have a degree of at most 4, appending to the lists should not be an issue.

    # iterate through the grid again
    for i in range(n1):
        for j in range(n2):
            if grid[i][j] in [1, 2]:
                index = coord_counter_map[(i, j)]
                if j > 0 and grid[i][j - 1] in [1,2]:
                    adj_list[index].append(coord_counter_map[(i, j - 1)])

                if j + 1 < n2 and grid[i][j + 1] in [1,2]:
                    adj_list[index].append(coord_counter_map[(i, j + 1)])

                if i > 0 and grid[i - 1][j] in [1,2]:
                    adj_list[index].append(coord_counter_map[(i - 1, j)])

                if i + 1 < n1 and grid[i + 1][j] in [1,2]:
                    adj_list[index].append(coord_counter_map[(i + 1, j)])

    distances = dict([(index, float('inf')) for index in range(counter)])

    for ri in rotten_indices:
        # perform bfs with the rotten index as a start
        # create a new 'visited' map for every iteration
        visited = dict([(v, False) for v in range(len(adj_list))])
        res = _graph_bfs(adj_list = adj_list, start_vertex=ri, visited=visited, result=[None for _ in adj_list])

        # save the minimum distance for each vertex
        for v, d in res:
            distances[v] = min(distances[v], d)

    final_result = 0
    for v, d in distances.items():
        final_result = max(final_result, d)

    if final_result == float('inf'):
        final_result = -1
    return final_result


"""
https://neetcode.io/problems/count-connected-components
"""
def countComponents(n: int, edges: List[List[int]]) -> int:
    # n: represents the number of nodes
    # e[i] = [a, b] => there is an edge between node 'a' and node 'b'
    # number of components ?
    
    # create the adjacency list first:
    counter = 0
    key_val = {}
    
    for (v1, v2) in edges:
        if v1 not in key_val:
            key_val[v1] = counter
            counter += 1

        if v2 not in key_val:
            key_val[v2] = counter
            counter += 1

    adj_list = [[] for _ in range(n)]   

    # iterate through edges
    for v1, v2 in edges:
        k1, k2 = key_val[v1], key_val[v2]
        adj_list[k1].append(k2)
        adj_list[k2].append(k1)

    return len(graph_connected_components(adj_list=adj_list))


"""
https://leetcode.com/problems/surrounded-regions/
"""
def solve(grid: List[List[str]]) -> None:
    """The main idea of this problem is to find connected components and capture components for which no vertex is on the edge of the board 

    Args:
        board (List[List[str]]): _description_
    """
    n1 = len(grid)
    n2 = len(grid[0])
    counter: int = 0

    coord_counter_map = {}
    counter_coord_map = {}
    # make sure to save the keys of vertices belonging to the edge
    edge_vertices = set()
    for i in range(n1):
        for j in range(n2):
            if grid[i][j] == 'O':
                if i in [0, n1 - 1] or j in [0, n2 - 1]:
                    edge_vertices.add(counter)
                coord_counter_map[(i, j)] = counter
                counter_coord_map[counter] = (i, j) 
                counter += 1

    # create an adjacency list
    adj_list = [[] for _ in range(counter)] # since a vertex can have a degree of at most 4, appending to the lists should not be an issue.

    # iterate through the grid again
    for i in range(n1):
        for j in range(n2):
            if grid[i][j] == 'O':
                index = coord_counter_map[(i, j)]

                # (i - 1, j) (i + 1, j) (i, j - 1), (i, j + 1)

                if j > 0 and grid[i][j - 1] == 'O':
                    adj_list[index].append(coord_counter_map[(i, j - 1)])

                if j + 1 < n2 and grid[i][j + 1] == 'O':
                    adj_list[index].append(coord_counter_map[(i, j + 1)])

                if i > 0 and grid[i - 1][j] == 'O':
                    adj_list[index].append(coord_counter_map[(i - 1, j)])

                if i + 1 < n1 and grid[i + 1][j] == 'O':
                    adj_list[index].append(coord_counter_map[(i + 1, j)])

    # now the adjacency list is ready
    components = graph_connected_components(adj_list=adj_list)
    for c in components:
        surrounded = True
        for vc in c:
            if vc in edge_vertices:
                surrounded = False
                break
        if surrounded:
            for vc in c:
                # convert the counter back to the coordinates
                i, j = counter_coord_map[vc]
                grid[i][j] = 'X'
    

def validTree(n: int, edges: List[List[int]]) -> bool:
    if len(edges) != n - 1:
        return False
    
    # the graph should be connected
    adj_list, _, _ = edgesList2adjList(n, edges)
    return is_graph_connected(adj_list=adj_list)



# def findRedundantConnection(edges: List[List[int]]) -> List[int]:
#     visited = {}
#     for v1, v2 in edges:
#         visited[v1] = False
#         visited[v2] = False
    
#     for v1, v2 in edges:
#         if visited[v1] and visited[v2]:
#             return [v1, v2]
        
#         visited[v1] = True 
#         visited[v2] = True
    
#     return [v1, v2]

def findRedundantConnection(edges: List[List[int]]) -> List[int]:
    # convert to the edges representations to the adjacency list
    # it is knowns that number of edges is equal to number of vertices
    adj_list, val_key, key_val = edgesList2adjList(len(edges), edges)
    
    visited = dict([(v, False) for v in range(len(adj_list))])
    queue = deque([0])
    
    visited[0] = True
    visited_by = {0:0}

    cv1, cv2 = None, None

    while len(queue) != 0:
        current_vertex = queue[0]
        for nv in adj_list[current_vertex]:
            if visited[nv] and nv != visited_by[current_vertex]:
                # it means we found our cycle
                cv1, cv2 = current_vertex, nv
                # empty the queue to end the upper loop
                while len(queue) != 0:
                    queue.pop()
                break            
            else:      
                visited[nv] = True
                visited_by[nv] = current_vertex
                queue.append(nv)

        if len(queue) != 0:
            queue.popleft()
        

    set1, set2 = set([cv1]), set([cv2])
    d1, d2 = deque([cv1, cv2]), deque([cv2])
    while True: 
        cv1, cv2 = visited_by[cv1], visited_by[cv2]
        set1.add(cv1)
        set2.add(cv2)
        d1.appendleft(cv1)
        d2.appendleft(cv2)
        if len(set1.intersection(set2)) != 0:
            break
    
    common_element = list(set1.intersection(set2))[0]
    # find the index of the common element in each of d1 and d2
    i1 = 0 
    for i1 in range(len(d1)):
        if d1[i1] == common_element:
            break
    i2 = 0
    
    for i2 in range(len(d2)):
        if d2[i2] == common_element:
            break

    # edges of the first cycle
    ec1 = [[key_val[d1[i]], key_val[d1[i + 1]]] for i in range(i1, len(d1) - 1)]
    ec2 = [[key_val[d2[i]], key_val[d2[i + 1]]] for i in range(i2, len(d2) - 1)]

    max_index = 0
    for ec in ec1:
        for index, e in enumerate(edges):
            if sorted(ec) == sorted(e):
                max_index = max(max_index, index)
                break

    for ec in ec2:
        for index, e in enumerate(edges):
            if sorted(ec) == sorted(e):
                max_index = max(max_index, index)
                break
    
    return edges[max_index]

