"""
Solving Tree Problems of level 1 according to this gfg guide: 

https://www.geeksforgeeks.org/top-50-tree-coding-problems-for-interviews/ 
"""

from typing import Tuple
from collections import defaultdict

class Node:
    def __init__(self,val):
        self.data = val
        self.left = None
        self.right = None


# https://www.geeksforgeeks.org/problems/height-of-binary-tree/1
def height(root: Node) -> int:
    # this function assumes that a tree with only one node: the "root" has a depth / height of "0"
    left_height, right_height = 0, 0
    
    if root.left is not None:
        left_height = 1 + height(root.left)

    if root.right is not None:
        right_height = 1 + height(root.right)
    
    return max(left_height, right_height)

def heigh_min1(root: Node) -> int:
    # this function assumes that a tree with only one node: the "root" has a depth / height of "1"
    left_height, right_height = 0, 0
    
    if root.left is not None:
        left_height = heigh_min1(root.left)

    if root.right is not None:
        right_height = heigh_min1(root.right)
    
    return 1 + max(left_height, right_height)


# https://www.geeksforgeeks.org/problems/determine-if-two-trees-are-identical/1
def isIdentical(r1: None, r2: None) -> bool:
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


# https://www.geeksforgeeks.org/problems/symmetric-tree/1

import math
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


# https://www.geeksforgeeks.org/problems/diameter-of-binary-tree/1
def diameter_depth(root: Node) -> tuple[int, int]:
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

def diameter(root: Node):
    # the idea here is to find the number of edges in the longest path in the 
    return diameter_depth(root)[0]

         
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
    # code here
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
    # code here
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
    # let's see how it all goes
    #code here
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


from collections import deque

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

