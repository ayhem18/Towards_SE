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
    # well this solution beats the hell out of 92% of other Python solutions NICE !!
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if subRoot is None:
            return True

        if root is None:
            return False

        if root.val == subRoot.val:
            if self.isSameTree(root, subRoot):
                return True

        if self.isSubtree(root.left, subRoot):
            return True

        if self.isSubtree(root.right, subRoot):
            return True

        return False

    # let's make things a bit more interesting and solve a 'medium' level problem
    # https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/description/
    # my solution isn't that fast apparently: beats only 20% of other solutions..
    def lowestCommonAncestorGeneral(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        queue = deque()
        queue.append(root)
        parent_mapper = {root: None}
        q_in, p_in = q == root, p == root
        shallow = None

        while len(queue) != 0 and not (q_in and p_in):
            node = queue.popleft()

            if node == q:
                q_in = True
                shallow = q if shallow is None else shallow

            if node == p:
                p_in = True
                shallow = p if shallow is None else shallow

            if node.left is not None:
                parent_mapper[node.left] = node
                queue.append(node.left)

            if node.right is not None:
                parent_mapper[node.right] = node
                queue.append(node.right)

        # define deep,
        deep = p if q == shallow else q
        shallow_ancestors = set()
        t = shallow
        while t is not None:
            shallow_ancestors.add(t)
            t = parent_mapper[t]

        # use the set above to find the
        t = deep
        while t is not None:
            if t in shallow_ancestors:
                return t
            t = parent_mapper[t]

        return t  # it will be None at this point

    # my solution above is general and does not utilize the fact that root represents a BINARY SEARCH TREE
    # where node.val > node.left.val and node.val <= node.val.right
    # well this solution is much better and uses the constraints of the problem

    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root == q or root == p:
            return root
        if min(q.val, p.val) < root.val < max(q.val, p.val):
            # this means that p and q are in different subtrees and automatically
            # the lowest ancestor will be 'root'
            return root

        if q.val > root.val and p.val > root.val:
            # it means they are both on the left subtree
            return self.lowestCommonAncestor(root.right, p, q)

        if q.val < root.val and p.val < root.val:
            # it means they are both on the left subtree
            return self.lowestCommonAncestor(root.left, p, q)

    # let's solve another one
    # https://leetcode.com/problems/binary-tree-level-order-traversal/
    def levelOrder(self, root: Optional[TreeNode]) -> list[list[int]]:
        # this problem is clearly BFS
        if root is None:
            return []
        queue = deque()
        queue.append(root)

        def level_generator():
            while len(queue) != 0:
                # save the length of the current queue before any modifications
                l = len(queue)
                yield [e.val for e in queue]
                for _ in range(l):
                    n = queue.popleft()
                    if n.left:
                        queue.append(n.left)
                    if n.right:
                        queue.append(n.right)

        res = [l for l in level_generator()]
        return res

    # the next one might seem a bit confusing at first, but it really isn't
    # https://leetcode.com/problems/binary-tree-right-side-view/
    def rightSideView(self, root: Optional[TreeNode]) -> list[int]:
        if root is None:
            return []
        queue = deque([root])

        def right_view_generator():
            while len(queue) != 0:
                # save the length of the current queue before any modifications
                l = len(queue)
                yield queue[-1].val
                for _ in range(l):
                    n = queue.popleft()
                    # most importantly put the left node first
                    if n.left:
                        queue.append(n.left)
                    if n.right:
                        queue.append(n.right)

        res = [r for r in right_view_generator()]
        return res

    # another 'medium' level problem
    # https://leetcode.com/problems/count-good-nodes-in-binary-tree/
    def nodes_higher_thresholds(self, root: TreeNode, threshold: int):
        if root is None:
            return 0
        left_score = self.nodes_higher_thresholds(root.left, max(root.left.val, threshold)) if root.left else 0
        right_score = self.nodes_higher_thresholds(root.right, max(root.right.val, threshold)) if root.right else 0
        return int(root.val >= threshold) + left_score + right_score

    def goodNodes(self, root: TreeNode) -> int:
        return self.nodes_higher_thresholds(root, root.val)
