"""
This script contains solutions to problems based on the traversal ideas: in-order, pre-order, post-order (not level-order traversal)
"""

import math
from collections import deque, defaultdict
from typing import Dict, List, Optional

from .utils_trees import Node, Index

def inorder_traversal(root: Node, l: Optional[deque] = None) -> List[int]:
    # left, root, right
    if l is None:
        l = deque()
    
    if root.left is not None:
        inorder_traversal(root.left, l)

    l.append(root.data)

    if root.right is not None:
        inorder_traversal(root.right, l)
    
    return l

def preorder_traversal(root: Node, l: Optional[deque] = None) -> List[int]:
    # left, root, right
    if l is None:
        l = deque()

    l.append(root.data)

    if root.left is not None:
        preorder_traversal(root.left, l)

    if root.right is not None:
        preorder_traversal(root.right, l)
    
    return l


def postorder_traversal(root: Node, l: Optional[deque] = None) -> List[int]:
    # left, root, right
    if l is None:
        l = deque()

    if root.right is not None:
        postorder_traversal(root.right, l)

    l.append(root.data)

    if root.left is not None:
        postorder_traversal(root.left, l)

    return l


# https://www.geeksforgeeks.org/problems/symmetric-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

# funny enough a binary tree is symmetric only and only iff, its inorder and postorder traversal are identical
def isSymmetric(root: Node) -> bool:
    q1, q2 = inorder_traversal(root), postorder_traversal(root)

    for i in range(len(q1)):
        if q1[i] != q2[i]:
            return False

    return True



# I misunderstood the problem: full does not mean having exactly 2 ** h - 1 nodes (where h is the height of the tree)
# but each tree has either 2 or 0 children...

def buildFullTreeRecursive(root: Node, preorder: List[int], pre_index: Index, level_by_index: Dict, root_level: int, max_level: int):
    # the first thing to consider is whether the node is a leaf or not
    if level_by_index[pre_index.index] == max_level:
        return

    if root.left is None:
        pre_index.increment()

        # initialize the left child object
        leftChild = Node(preorder[pre_index.index])
        # link it to the root
        root.left = leftChild
        
        level_by_index[pre_index.index] = root_level + 1

        buildFullTreeRecursive(root.left, preorder, pre_index, level_by_index, root_level + 1, max_level)

    # at this point we know that it is the right child of the current root 
    pre_index.increment()

    # initialize the left child object
    rightChild = Node(preorder[pre_index.index])
    # link it to the root
    root.right = rightChild
    

    level_by_index[pre_index.index] = root_level + 1

    return buildFullTreeRecursive(root.right, preorder, pre_index, level_by_index, root_level + 1, max_level)


# this is one is very tricky: my solution is very likely to be wrong... but who cares...
# https://www.geeksforgeeks.org/problems/construct-a-full-binary-tree--170648/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
def constructBinaryTree(pre, preMirror: List[int] = None, size: int = None):
    n = len(pre)
    # find the maximum level
    max_level = int(math.log(n + 1, 2))

    # create the root Node
    root = Node(pre[0])

    level_by_index = {0: 1}

    pre_index = Index()

    buildFullTreeRecursive(root=root, preorder=pre, pre_index=pre_index, level_by_index=level_by_index, root_level=1, max_level=max_level)

    return root
