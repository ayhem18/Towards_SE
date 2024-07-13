"""
This script contains my attempts to solve some gfg graph problems 
"""


from typing import List, Dict


def _dfs_cyclic_detection(adj_list: List[List[int]], start_vertex:int, visited: Dict) -> bool:
    visited[start_vertex] = True

    for v in adj_list[start_vertex]:
        if visited[v]:
            for vv in adj_list[v]:
                if visited[vv]:
                    return True        
        else:
            r = _dfs_cyclic_detection(adj_list, start_vertex=v, visited=visited)
            if r:
                return True
    return False




def isCyclic(num_v : int , adj : List[List[int]]) -> bool :
    """_summary_

    Args:
        num_v (int): number of vertices
        adj (List[List[int]]): adjacency list

    Returns:
        bool: whether the graph contains a cycle
    """
    counter = 0
    visited = dict([(i, False) for i in range(num_v)])
    
    while True:
        while counter < num_v and visited[counter]:
            counter += 1
        
        if counter == num_v:
            return False
        
        r = _dfs_cyclic_detection(adj_list=adj, start_vertex=counter, visited=visited)        
        
        if r:
            return True
    

if __name__ == '__main__':
    adj = [[1], [2, 3], [], [2]]
    print(isCyclic(len(adj), adj))
