"""
Solving Tree Problems of level 1 according to this gfg guide: 

https://www.geeksforgeeks.org/top-50-tree-coding-problems-for-interviews/ 
"""

from typing import Tuple, List
from collections import defaultdict
from easy import Node
from collections import deque


# https://www.geeksforgeeks.org/problems/construct-binary-tree-from-parent-array/1
def createTree(parent: List[int]) -> Node:
    parent_nodes = defaultdict(lambda : [])

    for i, v in enumerate(parent):
        parent_nodes[v].append(i)

    root = Node(parent_nodes[-1])

    queue = deque([root])
    
    while len(queue) != 0:
        node = queue.pop()

        children = parent_nodes[node.data]

        if len(children) > 0:
            # create the left node
            left_child = Node(children[0])
            node.left = left_child
            queue.append(left_child)
            
            if len(children) > 1:
                right_child = Node(children[1])
                node.right = right_child
                queue.append(right_child)

    return root
            