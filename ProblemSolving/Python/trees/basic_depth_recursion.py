"""
This script contains solutions to problems based on the idea of depth of a tree. The algorithm represents a sort of general trend

basically f(root) = {some code, f(right) (if exists), f(left) if exists}

it can be extended to have a function f that uses f_prime where f_prime returns both the value sought by f + another property of the subtree

"""

from typing import Dict, Optional, Tuple, Union, List
from collections import defaultdict

from .utils_trees import Node


########################################## BASIC RECURSIVE APPROACH ##########################################

# https://www.geeksforgeeks.org/problems/height-of-binary-tree/1
def height(root: Node) -> int:
    # this function assumes that a tree with only one node: the "root" has a depth / height of "0"
    left_height, right_height = 0, 0
    
    if root.left is not None:
        left_height = 1 + height(root.left)

    if root.right is not None:
        right_height = 1 + height(root.right)
    
    return max(left_height, right_height)


# https://www.geeksforgeeks.org/problems/determine-if-two-trees-are-identical/1
def isIdentical(r1: Node, r2: Node) -> bool:
    if (r1 is None) != (r2 is None):
        return False

    # consider the case where the tree is empty
    if r1 is None:
        return True

    # consider the values at the level of the root
    if r1.data != r2.data:
        return False
    
    # r1.left subtree is identical to r2.left subtree
    # r1.right subtree is identical to r2.left subtree
    return isIdentical(r1.left, r2.left) and isIdentical(r1.right, r2.right)


# https://www.geeksforgeeks.org/problems/mirror-tree/1
def mirror(root: Node):
    if root is None:
        return 
    
    temp = root.right
    root.right = root.left
    root.left = temp

    mirror(root.right)
    mirror(root.left)


def findNodeAndParentRecursive(root: Node, values: Union[List[int], set], value_node_map: Dict = None):
    # the main idea of this function is to find a certain node with a given value
    if not isinstance(values, set):
        values = set(values)

    if value_node_map is None:
        value_node_map = defaultdict(lambda : [])

    if root.left is not None:
        if root.left.data in values:
            value_node_map[root.left.data].append((root.left, root))
        findNodeAndParentRecursive(root.left, values=values, value_node_map=value_node_map)

    if root.right is not None:
        if root.right.data in values:
            value_node_map[root.right.data].append((root.right, root))
        findNodeAndParentRecursive(root.right, values=values, value_node_map=value_node_map)


def findNodeAndParent(root: Node, values: Union[List[int], set]):
    # first check if the root has one of the values we look for
    value_node_map = defaultdict(lambda : [])
    
    if root.data in values:
        value_node_map[root.data].append((root, None))
    
    # call the recursive function
    findNodeAndParentRecursive(root, values=values, value_node_map=value_node_map)

    return value_node_map

# https://www.geeksforgeeks.org/problems/max-and-min-element-in-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
def findMax(root: Node) -> int:
    left, right = -float("inf"), -float("inf")

    if root.left is not None:
        left = findMax(root.left)

    if root.right is not None:
        right = findMax(root.right)

    return max([root.data, left, right])

def findMin(root: Node) -> int:
    left, right = float("inf"), float("inf")

    if root.left is not None:
        left = findMin(root.left)

    if root.right is not None:
        right = findMin(root.right)

    return min([root.data, left, right])



########################################## EXTENDED-SUBTREE RECURSIVE APPROACH ##########################################

# when a certain property "P1" of the tree is dependent on a property P2 of a subtree, the main framework is to create a recursive function that
# returns both P1 and P2 () and wrap it around another function that returns only P1


# https://www.geeksforgeeks.org/problems/check-for-balanced-tree/1
def balance_depth(root: Node) -> Tuple[int, bool]:
    if root is None:
        return True, 0
    
    r_depth, l_depth = 0, 0

    if root.right is not None:
        r_b, r_depth = balance_depth(root.right)

        if not r_b:
            return False, 0   

        r_depth += 1

    if root.left is not None:
        l_b, l_depth = balance_depth(root.left)

        if not l_b:
            return False, 0 

        l_depth += 1

    return abs(l_depth - r_depth) <= 1, max(r_depth, l_depth)

def isBalanced(root):
    # the wrapper 
    return balance_depth(root)[0]



# https://www.geeksforgeeks.org/problems/children-sum-parent/1
def sumPropertyInner(root: Node) -> Tuple[bool, int]:
    if root is None:
        return True, 0
    
    r_sum, l_sum = 0, 0
    
    if root.right is not None:
        r_p, r_sum = sumPropertyInner(root.right)

        if not r_p:
            return False, 0

    if root.left is not None:
        l_p, l_sum = sumPropertyInner(root.left)

        if not l_p:
            return False, 0

    leaf_node = root.left is None and root.right is None

    return leaf_node or (root.data == l_sum + r_sum), root.data
    

def isSumProperty(root) -> bool:
    return sumPropertyInner(root)[0]



# https://www.geeksforgeeks.org/problems/check-for-bst/1
def bst_with_bounds(root: Node, min_val: float, max_val:float) -> bool:

    if min_val is None:
        min_val = -float("inf")

    if max_val is None:
        max_val = float("inf")

    if not (min_val <= root.data <= max_val):
        return False
    
    # the right subtree has root.data as a lower bound now and the inherited upper bound
    if root.right is not None:
        r_bst = bst_with_bounds(root.right, root.data, max_val)

        if not r_bst:
            return False
    
    if root.left is not None:
        l_bst = bst_with_bounds(root.left, min_val, root.data)
        
        if not l_bst:
            return False

    return True 

def isBST(root):
    return bst_with_bounds(root, None, None)



# https://www.geeksforgeeks.org/problems/array-to-bst4443/1
def sortedArrayToBST(nums):
    if len(nums) == 0:
        return None
    
    if len(nums) == 1:
        return Node(nums[0])

    root_index = len(nums) // 2
    root = Node(nums[root_index])   

    root.right = sortedArrayToBST(nums[root_index + 1:])
    root.left = sortedArrayToBST(nums[:root_index])

    return root


# https://www.geeksforgeeks.org/problems/kth-largest-element-in-bst/1
def k_largest_count(root: Node, k: int) -> Tuple[int, int]:
    root_count = 0
    
    if root.right is not None:
        right_count, right_res = k_largest_count(root.right, k)
        
        if right_res is not None:
            return right_count, right_res

        root_count += right_count

    if root_count == k - 1: 
        return root_count, root.data

    root_count += 1

    if root.left is not None:
        left_count, left_res = k_largest_count(root.left, k - root_count)

        if left_res is not None:
            return left_count, left_res
    
        root_count += left_count

    return root_count, None

def kthLargest(root: Node, k:int):
    return k_largest_count(root, k)[-1]


# https://www.geeksforgeeks.org/problems/foldable-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

def struct_symmetric(n1: Node, n2: Node) -> bool:
    if (n1.left is None) != (n2.right is None):
        return False
    
    if (n1.right is None) != (n2.left is None):
        return False
    

    if n1.left is not None:
        h = struct_symmetric(n1.left, n2.right)
        if not h:
            return False

    if n1.right is not None:
        h = struct_symmetric(n1.right, n2.left)
        if not h:
            return False

    return True


def IsFoldable(root: Node):
    if root is None:
        return True
    
    if (root.left is None) != (root.right is None):
        return False
    
    if root.left is None:
        return True
    
    # at this point we know that both root.left and root.right are present
    return struct_symmetric(root.left, root.right)


def diameter_depth(root: Node):
    if root is None:
        return 0, 0
    
    l_depth, r_depth = 0, 0
    r_diameter, l_diameter = 0, 0

    if root.left is not None:
        l_diameter, l_depth = diameter_depth(root.left)
        l_depth += 1

    if root.right is not None:
        r_diameter, r_depth = diameter_depth(root.right)
        r_depth += 1
    
    depth = max(l_depth, r_depth)

    return max(r_diameter, l_diameter, l_depth + r_depth), depth


# https://www.geeksforgeeks.org/problems/diameter-of-binary-tree/1
def diameter(self, root):
    # the diameter can be expressed as the maximum between the diameter of the right subtree, diameter of left subtree
    # or the sum of the depths of both subtress
    return diameter_depth(root)[0]


def lcaTuple(root: Node, n1: int, n2: int) -> Tuple[Optional[Node], Optional[Node], Optional[Node]]:
    n1_anc = None
    n2_anc = None

    if root.data == n1:
        n1_anc = root
    
    if root.data == n2:
        n2_anc = root

    if root.left is not None:
        left_lca, left_n1, left_n2 = lcaTuple(root.left, n1, n2)
        # which means that left_lca is indeed the lca of the values we are looking for
        if left_lca is not None:
            return left_lca, left_lca, left_lca

        if left_n1 is not None:
            n1_anc = root

        if left_n2 is not None:
            n2_anc = root

    if root.right is not None:
        right_lca, right_n1, right_n2 = lcaTuple(root.right, n1, n2)
    
        # which means that left_lca is indeed the lca of the values we are looking for
        if right_lca is not None:
            return right_lca, right_lca, right_lca

        if right_n1 is not None:
            n1_anc = root

        if right_n2 is not None:
            n2_anc = root

    if n1_anc is not None and n2_anc is not None:
        return root, root, root

    # otherwise the current root is not the lca    
    return None, n1_anc, n2_anc



def lca(root: Node, n1: int, n2: int) -> int:
    return lcaTuple(root, n1, n2)[0].data

