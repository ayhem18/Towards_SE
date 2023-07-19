"""
This script contains my solution for the leetCode problems of the Trees section
https://neetcode.io/roadmap
"""

from typing import Optional
from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# noinspection PyMethodMayBeStatic
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return root

        root.left, root.right = root.right, root.left

        if root.left:
            self.invertTree(root.left)
        if root.right:
            self.invertTree(root.right)

        return root

    # this is the most intuitive solution
    # but after watching the first minute of this video, I realized there are multiple ways,
    # and it must be instructive to experiment with several of them
    def maxDepthDFS(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        return 1 + max(self.maxDepthDFS(root.right), self.maxDepthDFS(root.left))

    # my bfs solution also works, nice !!
    # let's inspect the other main method to solve this problem
    # the 3rd solution is DFS with a stack, whic is basically the same
    # as the solution below
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # the key is to associate each node with its depth in the queue
        # took me some minutes to figure this out
        if root is None:
            return 0
        queue = deque()
        queue.append((root, 1))
        max_d = 1
        while len(queue) != 0:
            node, d = queue.popleft()
            d_plus1 = False
            if node.left is not None:
                queue.append((node.left, d + 1))
                d_plus1 = True

            if node.right is not None:
                queue.append((node.right, d + 1))
                d_plus1 = True

            max_d = max(max_d, d + int(d_plus1))

        return max_d

    # okay this is my solution for the Tree diameter problem
    # apparently, it isn't the best solution out there (well one of the worst...)
    # https://leetcode.com/problems/diameter-of-binary-tree/
    def all_nodes_depth(self, root: Optional[TreeNode], memo: dict = None) -> int:
        if memo is None:
            memo = {}
        if root is None:
            return 0
        d = 1 + max(self.all_nodes_depth(root.right, memo), self.all_nodes_depth(root.left, memo))
        memo[root] = d
        return d

    def diameterOfBinaryTreeMemo(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        # first let's find the depths of all trees
        memo = {}
        # pass memo to all_nodes_depth, so we can get the depth of each node in the BT
        self.all_nodes_depth(root, memo)
        # add None to memo
        memo[None] = 0
        p1 = memo[root.left] + memo[root.right]

        return max([p1, self.diameterOfBinaryTree(root.right), self.diameterOfBinaryTree(root.left)])

    # let me rewrite my solution for the Diameter problem
    # well this solution actually does the trick and beats around 80% of the solutions... NICE!!
    def diameter_and_depth(self, root: Optional[TreeNode]) -> tuple[int, int]:
        # depth, diameter
        if root is None:
            return 0, 0
        # let's first get the results of the subtrees
        left_depth, left_diameter = self.diameter_and_depth(root.left)
        right_depth, right_diameter = self.diameter_and_depth(root.right)

        root_depth = 1 + max(right_depth, left_depth)
        root_diameter = max([left_diameter, right_diameter, left_depth + right_depth])
        return root_depth, root_diameter

    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        depth, diameter = self.diameter_and_depth(root)
        return diameter

    # this is my solution for the balanced binary tree
    # https://leetcode.com/problems/balanced-binary-tree/
    def balance_and_depth(self, root: Optional[TreeNode]) -> tuple[int, bool]:
        if root is None:
            return 0, True

        left_height, left_balance = self.balance_and_depth(root.left)
        right_height, right_balance = self.balance_and_depth(root.right)

        return 1 + max(left_height, right_height), \
            (abs(left_height - right_height) <= 1 and left_balance and right_balance)

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        h, b = self.balance_and_depth(root)
        return b

    # this is my solution for this problem:
    # https://leetcode.com/problems/same-tree/
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # the first step is to eliminate the None object from the picture
        if p is None and q is None:
            return True

        if (p is None) != (q is None):
            return False

        # at this point of the code, neither p nor q is None
        if not p.val == q.val:
            return False

        if not self.isSameTree(p.right, q.right):
            return False

        return self.isSameTree(p.left, q.left)

    # this is my solution for this problem:
    # https://leetcode.com/problems/subtree-of-another-tree/
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        pass

