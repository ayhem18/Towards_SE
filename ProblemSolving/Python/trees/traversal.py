"""
This script contains solutions to problems based on the traversal ideas: in-order, pre-order, post-order (not level-order traversal)
"""

from collections import deque
from typing import List, Optional

from .utils_trees import Node

def inorder_tranversal(root: Node, l: Optional[deque] = None) -> List[int]:
    # left, root, right
    if l is None:
        l = deque()
    
    if root.left is not None:
        inorder_tranversal(root.left, l)

    l.append(root.data)

    if root.right is not None:
        inorder_tranversal(root.right, l)
    
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
    q1, q2 = inorder_tranversal(root), postorder_traversal(root)

    for i in range(len(q1)):
        if q1[i] != q2[i]:
            return False

    return True
