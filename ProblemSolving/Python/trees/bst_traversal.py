"""
This script contains my solutions to problems based on the idea of O(log(n)) traversal of a Binary Search Tree (or specific properties of bst in general...)
"""

from .utils_trees import Node

def min_val_bst(root: Node):
    element = root
    while element.left is not None:
        element = element.left
    
    return element


# https://www.geeksforgeeks.org/problems/inorder-successor-in-bst/1
def inorderSuccessor(root: Node, x: Node):
    if x.right is not None:
        return min_val_bst(x.right)

    element = root
    last_parent = None

    while element.data != x.data :
        if element.data < x.data:
            element = element.right

        elif element.data > x.data:
            last_parent = element
            element = element.left

    if last_parent is not None:
        return last_parent
    
    return None
