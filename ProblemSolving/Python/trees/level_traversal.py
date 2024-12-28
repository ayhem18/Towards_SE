"""
This script contain solutions to tree problems based on the idea of level-order traversal.
"""

import math

from typing import List, Tuple
from collections import deque, defaultdict
from .utils_trees import Node, tree_array_rep


def largestValues(root: Node):
    level_max = {}
    
    queue = deque([(0, root)])
    
    while len(queue) != 0:
        level, node = queue.pop()

        if level not in level_max:
            level_max[level] = node.data

        level_max[level] = max(node.data, level_max[level])

        if node.right is not None:
            queue.append((level + 1, node.right))           

        if node.left is not None:
            queue.append((level + 1, node.left))           

    return [level_max[i] for i in range(len(level_max))]



# https://www.geeksforgeeks.org/problems/symmetric-tree/1
def isSymmetric(root):
    if root is None:
        return True
    
    # build the array representation
    tree_array = tree_array_rep(root)
    tree_depth = int(math.ceil(math.log(len(tree_array), 2)))
    
    for i in range(1, tree_depth):
        a = tree_array[2 ** i - 1: 2 ** (i + 1) - 1]
        # make sure each level is palindrome
        for j in range(int(math.floor(len(a) / 2))):
            if a[j] != a[len(a) - 1 - j]:
                return False
            
    return True



# https://www.geeksforgeeks.org/problems/zigzag-tree-traversal/1
def zigZagTraversal(root: Node):   
    
    queue = deque([])
    stack = deque([(0, root)])

    total_count = 0
    count_map = {}

    current_level = 0
    current_level_count = 0

    level_count = defaultdict(lambda : 0)
    level_count[0] = 1

    while len(queue) != 0 or len(stack) != 0:
        if current_level_count == level_count[current_level]:
            current_level += 1
            current_level_count = 0

        current_level_count += 1

        if current_level % 2 == 0:
            level, node = stack.popleft()
        else:
            level, node = queue.pop()
        
        assert level == current_level

        count_map[total_count] = node.data
        total_count += 1

        if level % 2 == 0:
            if node.left is not None:
                queue.append((level + 1, node.left))           
                level_count[level + 1] += 1

            if node.right is not None:
                queue.append((level + 1, node.right))           
                level_count[level + 1] += 1

        else:                
            if node.right is not None:
                stack.appendleft((level + 1, node.right))           
                level_count[level + 1] += 1
            if node.left is not None:
                stack.appendleft((level + 1, node.left))           

                level_count[level + 1] += 1

    return [count_map[i] for i in range(len(count_map))] 



# https://www.geeksforgeeks.org/problems/right-view-of-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

def rightView(root: Node):
    # the idea of this problem is to find the rightmost node at each level
    # let's do the usual level-order traversal

    queue = deque([(0, root)])

    node_per_level = {}

    while len(queue) > 0:
        level, node = queue.popleft()   

        if node.left is not None:
            queue.append((level + 1, node.left))

        if node.right is not None:
            queue.append((level + 1, node.right))

        node_per_level[level] = node.data

    return [node_per_level[i] for i in range(len(node_per_level))]



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



# https://www.geeksforgeeks.org/problems/check-if-two-nodes-are-cousins/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
def isCousins(root: Node, a: int, b: int) -> bool:
    # the main goal of this problem is to determine whether the nodes with the given values 
    # are at the same level but with a different parent

    queue = deque([(0, root)])

    a_info = None
    b_info = None

    while len(queue) > 0:
        level, node = queue.popleft()   

        if node.left is not None:
            # check if the child has either the value 'a' or 'b'
            if node.left.data == a:
                a_info = (level + 1, node) 

            if node.left.data == b:
                b_info = (level + 1, node) 

            queue.append((level + 1, node.left))

        if node.right is not None:

            if node.right.data == a:
                a_info = (level + 1, node) 

            if node.right.data == b:
                b_info = (level + 1, node) 

            queue.append((level + 1, node.right))
    
    # check the root node as well
    if root.data == a:
        a_info = (0, None) 

    if root.data == b:
        b_info = (0, None) 

    if a_info is None or b_info is None:
        return False

    _, a_par = a_info
    _, b_par = b_info


    same_level = a_info[0] == b_info[0] 
    diff_parent = (a_par.data if a_par is not None else None) == (b_par.data if b_par is not None else None)

    return same_level and not diff_parent


# https://www.geeksforgeeks.org/problems/perfect-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
def isPerfect(root: Node) -> bool:
    # the main idea here is to do a level-order traversal and track the number of nodes per level

    nodes_per_level = defaultdict(lambda : 0)
    
    queue = deque([(0, root)])
    
    while len(queue) != 0:
        level, node = queue.pop()

        nodes_per_level[level] += 1 

        if node.right is not None:
            queue.append((level + 1, node.right))           

        if node.left is not None:
            queue.append((level + 1, node.left))           

    for level, nodes_count in nodes_per_level.items():
        if nodes_count != 2 ** level:
            return False
    
    return True



# https://www.geeksforgeeks.org/problems/complete-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_car
def isCompleteBT(root: Node) -> bool:
    # the main idea here is to make sure the level-order traversal is carried out from left to right at each level and add null nodes to the queue
    # the moment a null node is met
    # simply check whether the queue contains a non-null node
    # if so, return false, otherwise, the tree is complete

    queue = deque([root])

    while len(queue) > 0: 
        # make sure to pop from the left (FIFO mode)
        node = queue.popleft()
        
        if node is None:
            break

        queue.append(node.left)
        queue.append(node.right)
        
    # iterate through the queue
    for i in range(len(queue)):
        if queue[i] is not None:
            return False
        
    return True


# https://www.geeksforgeeks.org/problems/duplicate-subtree-in-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

def dupSub(root: Node) -> bool:
    # the idea here is to suck dick, like really really hard...
    leaf_parent_set = set()
    queue = deque([root])
    
    while len(queue) != 0:
        node = queue.popleft()
        
        if node.left is not None:
            c = node.left
            
            if c.left is None and c.right is None:
                # this means 'c' is a leaf node
                c_signature = (c.data, node.data, 'l')
                if c_signature in leaf_parent_set:
                    return True
                leaf_parent_set.add(c_signature)

            # add it to the queue
            queue.append(node.left)                 

        if node.right is not None:
            c = node.right
            
            if c.left is None and c.right is None:
                # this means 'c' is a leaf node
                c_signature = (c.data, node.data, 'r')
                if c_signature in leaf_parent_set:
                    return True
                leaf_parent_set.add(c_signature)

            # add it to the queue
            queue.append(node.right)                 

    return False
