from typing import List, Dict, Optional, Tuple
from collections import deque

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

    components = []
    
    while count_vis < n_vertices:
        while start_vertex < n_vertices and visited[start_vertex]:
            start_vertex += 1

        # this means we visited all vertices
        if start_vertex == n_vertices:
            break

        component_vertices = graph_dfs(adj_list=adj_list, start_vertex=start_vertex, visited=visited)
        components.append(component_vertices)

    return components

def _graph_bfs(adj_list: List[List[int]], 
               start_vertex: int, 
               visited: Dict, 
               result: List[Tuple[int, int]] = None):

    if result is None:
        result = [None for _ in adj_list]

    queue = deque([(start_vertex, 0)])
    visited[start_vertex] = True    
    counter = 0

    while len(queue) != 0:
        current_vertex, dis = queue[0]
        result[counter] = (current_vertex, dis)
        counter += 1
        for v in adj_list[current_vertex]:
            if not visited[v]:
                visited[v] = True
                queue.append((v, dis + 1))

        queue.popleft()

    res = [r for r in result if r is not None]
    return res 


# write a function to determine whether a graph is connected
def is_graph_connected(adj_list: List[List[int]]) -> bool:
    n_vertices = len(adj_list)    
    # create the visited dict
    visited = dict([(v, False) for v in range(len(adj_list))])
    start_vertex = 0
    component_vertices = graph_dfs(adj_list=adj_list, start_vertex=start_vertex, visited=visited)
    return len(component_vertices) == n_vertices


# write a function to convert from the edges list to adjacency list
def edgesList2adjList(n: int, edges:List[List]) -> Tuple[List[List], Dict]:
    counter = 0
    key_val = {}
    val_key = {}
    for (v1, v2) in edges:
        if v1 not in val_key:
            val_key[v1] = counter
            key_val[counter] = v1
            counter += 1
            
        if v2 not in val_key:
            val_key[v2] = counter
            key_val[counter] = v2
            counter += 1

    adj_list = [[] for _ in range(n)]   

    # iterate through edges
    for v1, v2 in edges:
        k1, k2 = val_key[v1], val_key[v2]
        adj_list[k1].append(k2)
        adj_list[k2].append(k1)

    return adj_list, val_key, key_val


