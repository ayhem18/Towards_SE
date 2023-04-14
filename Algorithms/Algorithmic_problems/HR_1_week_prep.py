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


# first let's determine the possible combination of bricks
import numpy as np


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


def build_linked_list(values: list[int]):
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


def possible_combinations(m: int, values: set):
    # create the table that will store the results
    table = [[] for _ in range(m + 1)]
    min_val = min(values)
    for i in range(min_val, m + 1):
        # append the rest of the results
        for j in values:
            if i >= j:
                # extract the possible sub combinations
                sub_combinations = table[i - j]
                if sub_combinations:
                    table[i].extend([[j] + sub_c for sub_c in sub_combinations])
                else:
                    table[i].append([j])

    # now just extract the possible combinations for the last element: n
    return table[m]


def can_be_consecutive(seq1: list, seq2: list):
    pass
    i1, i2 = 0, 0
    count1, count2 = 0, 0
    defect_points = set()
    while i1 != len(seq1) or i2 != len(seq2):
        if count1 == count2:
            defect_points.add(count1)
        if count1 > count2:
            count2 += seq2[i2]
            i2 += 1
        else:
            count1 += seq1[i1]
            i1 += 1

    # remove 0 and the sum of all elements
    defect_points.discard(sum(seq1))
    defect_points.discard(0)

    if defect_points == set():
        return True, defect_points

    return False, defect_points


def build_defect_pairs(one_row_combinations):
    non_consecutive_combinations = {}
    # now determine which combinations cannot be consecutive
    for i1, com1 in enumerate(one_row_combinations):
        s1 = " ".join([str(c) for c in com1])
        for i2 in range(i1, len(one_row_combinations)):
            com2 = one_row_combinations[i2]
            s2 = " ".join([str(c) for c in com2])
            res, defect_points = can_be_consecutive(com1, com2)
            if not res:
                if s1 in non_consecutive_combinations:
                    non_consecutive_combinations[s1].append((com2, defect_points))
                else:
                    non_consecutive_combinations[s1] = [(com2, defect_points)]

                if s1 != s2:
                    if s2 in non_consecutive_combinations:
                        non_consecutive_combinations[s2].append((com1, defect_points))
                    else:
                        non_consecutive_combinations[s2] = [(com1, defect_points)]

    # make sure each combination is present at least once
    for com in one_row_combinations:
        com_string = " ".join([str(c) for c in com])
        if com_string not in non_consecutive_combinations:
            non_consecutive_combinations[com_string] = [([], set())]

    return non_consecutive_combinations


BIG_INTEGER = 10 ** 9 + 7


def invalid_combinations(n: int, initial_combinations: list[list], defect_points: set, pairs: dict):
    # first of all check if  we have non-empty initial_combinations and defect_points
    if n <= 1 or len(initial_combinations) == 0 or len(defect_points) == 0:
        return 0

    result = 0
    # the base case is 2
    if n == 2:
        for combination in initial_combinations:
            # extract the string representation of the combination
            com_string = " ".join([str(c) for c in combination])
            next_list = pairs[com_string]
            # filter those that do not have defects
            result += len([n for n in next_list if len(n[0]) != 0])

        return result % BIG_INTEGER

    result = 0
    for combination in initial_combinations:
        # extract the string representation of the combination
        com_string = " ".join([str(c) for c in combination])
        next_list = pairs[com_string]
        for com, dp in next_list:
            result += invalid_combinations(n - 1, com, defect_points.intersection(dp), pairs) % BIG_INTEGER

    return result


# let's build our final function
OUR_SET = {1, 2, 3, 4}


def legoBlocks(n, m):

    # first extract all the possible combinations
    one_row_combinations = possible_combinations(m, OUR_SET)

    x = len(one_row_combinations)
    # second calculate the theoretical number of all possible combinations: len(one_row_combinations) ** n

    total = 1
    for _ in range(n):
        total = (total * x) % BIG_INTEGER

    pairs = build_defect_pairs(one_row_combinations)

    total_invalid = invalid_combinations(n, one_row_combinations, set(list(range(1, m))), pairs)
    # now simply count the number of stuff on this
    return (total - total_invalid) % BIG_INTEGER


import pprint
def main():
    pp = pprint.PrettyPrinter(sort_dicts=True)

    # p = possible_combinations(2, OUR_SET)
    # c_combinations = build_defect_pairs(p)
    # pp.pprint(p)
    # pp.pprint(c_combinations)


    res = legoBlocks(3, 2)
    pp.pprint(res)


if __name__ == '__main__':
    main()
