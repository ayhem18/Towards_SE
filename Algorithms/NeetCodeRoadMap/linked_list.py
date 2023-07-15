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
        del(d[0])

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


if __name__ == '__main__':
    sol = Solution()
    l = sol.linked_list_from_list([1, 2, 3, 4, 5, 6])
    sol.reorderList(l)
    sol.traverse_linked_list(l, display=True)
