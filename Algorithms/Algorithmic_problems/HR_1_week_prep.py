import math
import os
import random
import re
import sys


def minimumBribes(queue):
    total_count = 0  # the total number of bribes

    while len(queue) > 0:
        count = queue[0] - 1
        if count > 2:
            print('Too chaotic')
            return

        for index in range(1, len(queue)):
            if queue[index] > queue[0]:
                queue[index] = queue[index] - 1
        # add the count to the total
        total_count += count
        queue = queue[1:]

    print(total_count)
    # return total_count


def fun(p_d):
    N = len(p_d)
    # first determine the difference
    diffs = [pair[0] - pair[1] for pair in p_d]

    def next_index(i, N):
        return (i + 1) % N

    def cycle(index):
        i = next_index(index, N)
        petrol = diffs[index]
        while petrol >= 0 and i != index:
            petrol += diffs[i]
            i = next_index(i, N)
        if petrol >= 0:
            return True, index
        return False, i

    station_index = 0
    while station_index < N:
        res_bool, res_index = cycle(station_index)
        if res_bool:
            return res_index
        else:
            station_index = res_index
    # if the code reaches this
    return -1


class SinglyLinkedListNode:
    pass


class SinglyLinkedListNode:
    def __init__(self, data: int, next: SinglyLinkedListNode = None):
        self.data = data
        self.next = next


def mergeLists(head1: SinglyLinkedListNode, head2: SinglyLinkedListNode):
    # head1 /head 2 represent the heads of  sorted linked lists
    # first let's eliminate the possibility of empty lists
    if head1 is None:
        return head2

    if head2 is None:
        return head1

    # now both lists have at least one element
    p1 = head1
    p2 = head2

    if p1.data < p2.data:
        new_head = p1
        p1 = p1.next
    else:
        new_head = p2
        p2 = p2.next

    p = new_head
    # now time to build the new linked list
    while p1 is not None and p2 is not None:
        if p1.data < p2.data:
            p.next = SinglyLinkedListNode(p1.data)
            p1 = p1.next
        else:
            p.next = SinglyLinkedListNode(p2.data)
            p2 = p2.next

        p = p.next

    # now one of the lists is empty
    if p1 is None:
        p.next = p2
    else:
        p.next = p1

    return new_head


def build_linked_list(values:list[int]):
    assert values
    head = SinglyLinkedListNode(values[0])
    p = head
    for i in range(1, len(values)):
        next_node = SinglyLinkedListNode(values[i])
        p.next = next_node
        p = p.next
    return head


def traverse_linked_list(head):
    traverse = head
    while traverse is not None:
        print(traverse.data)
        traverse = traverse.next


def play_with_linked_lists():
    # v1 = list(range(1, 10, 2))
    v2 = list(range(2, 15, 2))
    v1 = None
    l1 = build_linked_list(v2)
    l2 = build_linked_list(v2)
    print("list 1", end='\n')
    traverse_linked_list(l1)
    print("list 2", end='\n')
    traverse_linked_list(l2)
    # let's see them merge
    new_linked_list = mergeLists(l1, l2)
    print("merged list")
    traverse_linked_list(new_linked_list)


def _binary_search(array: list, x, low, high):
    while low <= high:

        mid = low + (high - low) // 2

        if array[mid] == x:
            return mid

        elif array[mid] < x:
            low = mid + 1

        else:
            high = mid - 1

    return -1


def binary_search(array: list, x):
    return _binary_search(array, x, 0, len(array) - 1)


def pairs(target, values):
    # first sort the values
    values = sorted(values)
    freq_counter = {}
    for v in values:
        if v in freq_counter:
            freq_counter[v] += 1
        else:
            freq_counter[v] = 1

    if target == 0:
        return int(sum([(n * (n - 1)) / 2 for _, n in freq_counter.items()]))

    count = 0
    for index, v in enumerate(values):
        index_result = binary_search(values, v + target)
        if index_result > index:
            count += freq_counter[v + target]

    return count


def main():
    t = 1
    values = [1, 1, 1, 2, 2, 3, 1, 4, 10]
    print(pairs(t, values))

if __name__ == '__main__':
    main()
