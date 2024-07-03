from typing import List, Tuple
def successor(num: List[int]) -> List[int]:
    n = len(num)
    res = num.copy()

    c = 1
    for i in range(n): 
        add_res = res[i] + c
        c = int(add_res >= 3)
        res[i] = (add_res % 3)
        if c == 0:
            break
        
    if c != 0:
        res.append(1)

    return res

def rep2int(rep: List[int]) -> int:
    res = 0
    exp = 1
    for value in rep:
        res += exp * value
        exp *= 3
    
    return res

import math
def log_3(a: int) -> int: 
    return int(math.log(a, 3))


def int2rep(a: int) -> List[int]:
    if a == 0:
        return [0]

    res = []
    n = log_3(a)
    for i in range(n, -1, -1):
        bit = a // (3 ** i)
        a = a - bit * (3 ** i)
        res.insert(0, bit)

    return res


def leq(a: List[int], b: List[int]) -> bool:
    # first we need to find the most significant bit from each list
    n1, n2 = len(a), len(b)
    i1, i2 = None, None
    for i in range(n1 - 1, -1, -1):
        if i != 0:
            i1 = i
            break

    for i in range(n2 - 1, -1, -1):
        if i != 0:
            i2 = i
            break

    if i1 is None:
        # this means that a is 0 (which should be smaller or equal to any other non-nge number)
        return True

    if i2 is None:
        # a is not zero at this point of the program
        return False

    if i1 < i2:
        # this automatically means that log_3(a) is less than log_3(b)
        return True
    
    if i2 < i1:
        return False

    # at this point we know that, both of them have the log3 (rounded to int)
    for i in range(i1, -1, -1):
        if a[i] > b[i]:
            return False
        if b[i] > a[i]:
            return True
    
    # reaching this point means a == b
    return True


def calibrate(a: List[int], b:List[int]) -> Tuple[List[int]]:
    n1, n2 = len(a), len(b)
    max_len = max(n1, n2)
    if len(a) != max_len:
        a = a + [0 for _ in range(max_len - n1)]

    if len(b) != max_len:
        b = b + [0 for _ in range(max_len - n2)]

    return a, b


def trim(a: List[int]) -> List[int]:
    n1 = len(a)
    i1 = 0
    for i in range(n1 - 1, -1, -1):
        if a[i] != 0:
            i1 = i
            break
    
    return a[:i1 + 1]

def tritwise_min(a: List[int], b:List[int]) -> List[int]:
    a, b = calibrate(a, b)
    temp_res = ([min(i, j) for i, j in zip(a, b)])    
    res = trim(temp_res)
    return res


def f(a: List[int], b: List[int]) -> List[int]:
    current = a
    res = current   
    succ = current

    if a == b:
        return a

    while (leq(current, b)):
        res = tritwise_min(res, succ)
        succ = successor(current)
        current = succ
    return res

def f_eff(a: List[int], b: List[int]) -> List[int]:
    # calibrate
    a, b = calibrate(a, b)

    if a == b:
        return a

    n = len(a)
    res = [0 for _ in range(n)]
    # find the most significant position in 'a' 
    
    a_index = None
    for i in range(n - 1, -1, -1):
        if a[i] != 0:
            a_index = i
            break
    

    if a_index is None:
        # this mean 'a' is zero
        # the result will also be zero
        return trim(res)


    b_index = None
    for i in range(n - 1, -1, -1):
        if b[i] != 0:
            b_index = i
            break
    

    if b_index is None:
        # this mean 'a' is zero
        # the result will also be zero
        return trim(res)


    if b_index != a_index:
        return trim(res)

    i = b_index 
    while a[i] == b[i]:
        res[i] = a[i]
        i -= 1
    
    # at this point we know that a[i] != b[i] (no need to worry about i going out of bounds, since a != b)
    res[i] = a[i]
    # the rest of the indices have to be 0
    return trim(res)

if __name__ == '__main__':
    for i in range(10, 300):
        if 3 ** int(log_3(i)) == i:
            continue

        repi = int2rep(i)
        for j in range(1, i + 1):
            # i = 11 
            # j = 10
            repi = int2rep(i)
            repj = int2rep(j)
            r1 = f(repj, repi) 
            r2 = f_eff(repj, repi)
            assert r1 == r2, "check"
    # for i in range(15):
    #     repi = int2rep(3 ** i)   
    #     print(repi)
