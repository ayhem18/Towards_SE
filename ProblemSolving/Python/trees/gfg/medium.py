"""
Solving Tree Problems of level 1 according to this gfg guide: 

https://www.geeksforgeeks.org/top-50-tree-coding-problems-for-interviews/ 
"""

from typing import Tuple, List
from collections import defaultdict
from collections import deque
from trees.gfg.easy import Node


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


# https://www.geeksforgeeks.org/problems/bottom-view-of-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

def bottomView(root: Node):
    # once again using basic ideas from level order traversal
    queue = deque([(0, 0, root)]) # each element will save (level, position, node)

    node_per_position = {}

    min_position, max_position = float('inf'), -float('inf')

    while len(queue) > 0:
        level, position, node = queue.popleft()   

        if node.left is not None:
            queue.append((level + 1, position - 1, node.left))

        if node.right is not None:
            queue.append((level + 1, position + 1, node.right))

        node_per_position[position] = node.data

        min_position = min(min_position, position)
        max_position = max(max_position, position)

    
    return [node_per_position[i] for i in range(min_position, max_position + 1)]

