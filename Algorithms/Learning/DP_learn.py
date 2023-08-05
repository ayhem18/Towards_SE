"""
in this script I practice a number of standard Dynamic Programming problems, to better understand the concept.
This is based on the YouTube course: https://www.youtube.com/watch?v=oBt53YbR9Kk&t=4s
"""

import numpy as np
from typing import Union, List


# let's start with something very simple such as Fibonacci numbers
def fib_rec(n: int):
    if n <= 2:
        return 1
    return fib_rec(n - 1) + fib_rec(n - 2)


# let's solve this problem by memoization
def fib(n: int, memo: dict = None) -> int:
    # python stuff
    memo = {} if memo is None else memo
    # first check if n is in memo
    if n in memo:
        return memo[n]

    # usual base-case
    if n <= 2:
        return 1

    # 2 main things:
    # make sure to pass the momo object to the recursive calls: (otherwise what's the point ?)
    # make sure to save the result in memo
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]


## let's consider the grid traveler problem
def grid_rec(n: int, m: int) -> int:
    min_n = min(n, m)
    max_n = max(n, m)

    if min_n == 1 and max_n == 1:
        return 1

    if min_n < 1:
        return 0

    return grid_rec(min_n - 1, max_n) + grid_rec(min_n, max_n - 1)


def grid_rec_memo(n: int, m: int, memo: dict = None) -> int:
    min_n = min(n, m)
    max_n = max(n, m)

    if memo is None:
        memo = {}

    # no need to check for the children if the recursive call starts with
    # checking the memo object
    if (min_n, max_n) in memo:
        return memo[(min_n, max_n)]

    if min_n == 1 and max_n == 1:
        return 1

    if min_n < 1:
        return 0

    # make sure to pass the memo object to the recursive calls
    memo[(min_n, max_n)] = grid_rec_memo(min_n - 1, max_n, memo=memo) + grid_rec_memo(min_n, max_n - 1, memo=memo)
    return memo[(min_n, max_n)]


# let's consider the following problem
def canSum(target: int, coins: List[int]) -> bool:
    pass


# let's consider the recursive version of the can sum function: determines whether
# a target value can be a sum of elements of a given array where each element
# can be sampled as many times as needed
def can_sum_rec(target: int, values: list[int]) -> bool:
    assert target >= 0 and all([v >= 0 for v in values])
    # first let's consider the main base case:
    if target < min(values):
        return False

    for v in values:
        if target % v == 0:
            return True

    final_res = False
    for v in values:

        # if the target - v can be expressed as a sum of elements of the array, then so target
        final_res = v <= target and can_sum_rec(target - v, values)
        if final_res:
            break

    return final_res


# let's implement the same problem using memoization
def can_sum_memo(target: int, values: list[int], memo: dict = None) -> bool:
    # first the python thingy with reference objects
    if memo is None:
        memo = {}

    if target in memo:
        return memo[target]

    if target < min(values):
        return False

    for v in values:
        if target % v == 0:
            return True

    final_res = False
    for v in values:
        # if the target - v can be expressed as a sum of elements of the array, then so target
        final_res = v <= target and can_sum_memo(target - v, values, memo=memo)
        if final_res:
            break

    # make sure to save the object to the memo
    memo[target] = final_res
    return memo[target]


# The code above is mine. Nevertheless, the code on the YouTube course is much simpler and probably more efficient
def can_sum(n: int, numbers: list[int], memo: dict = None) -> bool:
    # python initialization thingy
    if memo is None:
        memo = {}
    # if the result is encountered previously
    if n in memo:
        return memo[n]

    if n == 0:
        return True

    if n < 0:
        return False

    for num in numbers:
        temp = can_sum(n - num, numbers, memo=memo)
        memo[n - num] = temp
        if temp:
            return True

    # only return False if all sub-cases return False
    # save the result for n
    memo[n] = False
    return False


# The code above is mine. Nevertheless, the code on the YouTube course is much simpler and probably more efficient
def how_sum(n: int, numbers: list[int], memo: dict = None) -> Union[None, list[int]]:
    # python initialization thingy
    if memo is None:
        memo = {}
    # if the result is encountered previously
    if n in memo:
        return memo[n]

    if n == 0:
        return []

    if n < 0:
        return None

    for num in numbers:
        temp = how_sum(n - num, numbers, memo=memo)
        if temp is not None:
            memo[n - num] = [num] + temp
            return memo[n - num]

    # only return False if all sub-cases return False
    # save the result for n
    memo[n] = None
    return None


if __name__ == '__main__':
    # let's test the code really quick
    for t in range(1, 10000):
        values = np.random.randint(low=2, high=1000, size=(20,))
        values = sorted(list(values), reverse=True)

        b1 = can_sum(t, values)
        b2 = how_sum(t, values)
        try:
            assert b1 == (b2 is not None), "One of your functions is acting weird"
            if b2 is not None:
                assert t == sum(b2)
            if t % 1000 == 0:
                print(t)
                print(b2)

        except AssertionError:
            print(t)
            print(b1)
            print(b2)
