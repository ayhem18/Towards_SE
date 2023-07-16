"""
This script contains my solutions for the NeetCode problems for the linked List section:
https://neetcode.io/roadmap
"""
from typing import Optional, Union
from copy import copy


# Definition for singly-linked list, given by LeetCode

class ListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next = next_node


# Definition for a Node.
class Node:
    def __init__(self, x: int, next_node: 'Node' = None, random_node: 'Node' = None):
        self.val = int(x)
        self.next = next_node
        self.random = random_node


# noinspection PyMethodMayBeStatic
class Solution:
    def traverse_linked_list(self, head: Optional[ListNode],
                             display: bool = False) -> Optional[ListNode]:
        if head is None:
            return head
        t = copy(head)
        while t.next is not None:
            if display:
                print(t.val)
            t = t.next

        # to display the last element
        if display:
            print(t.val)

        return t

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        # now the list have at least 2 nodes
        head_copy = copy(head)
        head_copy.next = None

        t = copy(head)
        t = t.next
        while t.next is not None:
            # create a new node
            new_node = ListNode(t.val)
            new_node.next = head_copy
            head_copy = new_node
            # don't forget to update the traversing node
            t = t.next

        # t now is the last element in the list
        t.next = head_copy
        return t

    def linked_list_from_list(self, seq: list[Union[int, float]]) -> Optional[ListNode]:
        if len(seq) == 0:
            return None

        head = ListNode(seq[0])
        current_head = head
        for v in seq[1:]:
            current_head.next = ListNode(val=v)
            current_head = current_head.next

        return head

    # merge 2 linked lists
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # let's merge some linked lists
        if list1 is None:
            return list2
        elif list2 is None:
            return list1
        # now we are sure that neither lists are Nones
        t1, t2 = copy(list1), copy(list2)
        if t1.val < t2.val:
            head = t1
            t1 = t1.next
        else:
            head = t2
            t2 = t2.next
        t = head

        while t1 is not None and t2 is not None:
            if t1.val < t2.val:
                t.next = t1
                t1 = t1.next
            else:
                t.next = t2
                t2 = t2.next
            t = t.next

        t.next = t2 if t1 is None else t1

        return head

    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # let's remove the degenerate cases from the way
        if head is None or head.next is None:
            return head

        d = {}
        index = 0
        t = copy(head)

        while t is not None:
            d[index] = t
            t = t.next
            index += 1

        p1, p2 = 1, index - 1

        # remove the head
        del (d[0])

        t = head
        while len(d) != 0:
            if p2 in d:
                t.next = d[p2]
                t = t.next
                # remove the element from the dict
                del d[p2]
                p2 -= 1
            if p1 in d:
                t.next = d[p1]
                t = t.next
                # remove the element from the dict
                del d[p1]
                p1 += 1

        t.next = None

    # another medium problem for the fun of it:
    # https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        if head is None:
            return head
        index = 0
        t = head
        while t is not None:
            t = t.next
            index += 1

        N = index
        # this is the case where the head is removed
        if N == n:
            return head.next

        counter = 0
        t = head
        while True:
            if counter == N - n - 1:
                # this means the node to be removed is the last node
                if n == 1:
                    t.next = None
                else:
                    t.next = t.next.next
                break
            t = t.next
            counter += 1

        return head

    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # let's start by removing the degenerate cases
        if head is None:
            return head

        # there is only one element in the node
        if head.next is None:
            new_head = copy(head)
            if head.random is not None:
                new_head.random = new_head
            return new_head
        # the main idea is to build an index to index map: mapping the node of each index
        # to the random_node's index
        index_to_id = {}
        id_to_index = {}
        id_to_random_id = {}
        index = 0
        t = head
        while t is not None:
            idt = id(t)
            index_to_id[index] = idt
            id_to_index[idt] = index
            # access the random node pointed by 't'
            if t.random is not None:
                id_random = id(t.random)
                id_to_random_id[idt] = id_random
            index += 1
            t = t.next
        # now we need to construct index_to_random_index map

        index_to_random_index = {}
        for node_index, node_id in index_to_id.items():
            if node_id in id_to_random_id:
                random_node_id = id_to_random_id[node_id]
                random_index = id_to_index[random_node_id]
                index_to_random_index[node_index] = random_index

        # now time to build the new linked list
        new_head = copy(head)
        new_t = new_head
        t = head.next

        # a new a dictionary that maps indices to the actual nodes
        counter = 1
        index_to_node = {0: new_head}

        while t is not None:
            # create the new node
            new_node = Node(t.val)
            # add the new_node to new_t
            new_t.next = new_node
            new_t = new_node
            # make sure to map the counter to the new node
            index_to_node[counter] = new_node
            # update the counter
            counter += 1
            # update t
            t = t.next

        # another pass on the data
        t = new_head
        index = 0
        while t is not None:
            if index in index_to_random_index:
                # this means the current node points to an actual node
                # extract the node index
                random_node_index = index_to_random_index[index]
                t.random = index_to_node[random_node_index]
            else:
                t.random = None

        return new_head

    def to_ll(self, n: int) -> ListNode:
        new_head = ListNode(val=int(n % 10))
        n = n // 10
        t = new_head
        while n > 0:
            new_node = ListNode(val=int(n % 10))
            t.next = new_node
            t = t.next
            n = n // 10
        return new_head

    def to_int(self, head: ListNode) -> int:
        index = 0
        t = head
        n = 0
        while t is not None:
            n += t.val * 10 ** index
            t = t.next
            index += 1
        return n

    # proud of this solution though:
    # https://leetcode.com/problems/add-two-numbers/
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        return self.to_ll(self.to_int(l1) + self.to_int(l2))

    def hasCycleN_memo(self, head: Optional[ListNode]) -> bool:
        # let's start with a simple solution: O(n) memory
        seen_nodes = set()
        t = head

        while t is not None:
            if t in seen_nodes:
                return True
            seen_nodes.add(t)
            t = t.next

        return False

    # let's try to solve the follow-up question:
    # is it possible to solve it in O(1) memory
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        if head is None:
            return False

        if head.next is None:
            return head.next == head

        # first let's define p1 and p2
        p1, p2 = head, head.next
        counter = 0
        while p2 is not None:
            if p1 == p2:
                return True

            p2 = p2.next
            if counter % 2 == 0:
                p1 = p1.next
            counter += 1

        return False


if __name__ == '__main__':
    sol = Solution()
    l1 = sol.to_ll(101)
    l2 = sol.to_ll(456)

    sol.traverse_linked_list(l1, display=True)
    print("#" * 100)
    sol.traverse_linked_list(l2, display=True)
    print("#" * 100)
    res = sol.addTwoNumbers(l1, l2)
    sol.traverse_linked_list(res, display=True)
