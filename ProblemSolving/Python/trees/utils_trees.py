"""
a small script for Tree utility functions
"""
from typing import Optional

class Node:
    def __init__(self,val):
        self.data = val
        self.left = None
        self.right = None



# HEIGHT OF A TREE !!! (ONE NODE TREE WITH HEIGHT 1)
def heigh_min1(root: Node) -> int:
    # this function assumes that a tree with only one node: the "root" has a depth / height of "1"
    left_height, right_height = 0, 0
    
    if root.left is not None:
        left_height = heigh_min1(root.left)

    if root.right is not None:
        right_height = heigh_min1(root.right)
    
    return 1 + max(left_height, right_height)

# NUMBER OF NODES IN A TREE
def getSize(root : Optional['Node']) -> int:
    if root is None:
        return 0
    
    total = 1
    if root.left is not None:
        total += getSize(root.left)

    if root.right is not None:
        total += getSize(root.right)

    return total

def fill_tree_array(node: Node, node_index: int, tree: list):
    if node is None:
        if node_index < len(tree):
            tree[node_index] = None

            if len(tree) > 2 * node_index + 1:
                tree[2 * node_index + 1] = None

                if len(tree) > 2 * node_index + 2:
                    tree[2 * node_index + 2] = None

        return 

    tree[node_index] = node.data
    fill_tree_array(node.left, node_index * 2 + 1, tree)
    fill_tree_array(node.right, node_index * 2 + 2, tree)


def tree_array_rep(root: Node):
    if root is None:
        return []

    # first find the depth of the tree
    tree_depth = heigh_min1(root)
    array = [None for _ in range(2 ** tree_depth - 1)]

    fill_tree_array(root, node_index=0, tree=array)
    return array        


class Index:
    def __init__(self):
        self.index = 0

    def increment(self):
        self.index += 1
        