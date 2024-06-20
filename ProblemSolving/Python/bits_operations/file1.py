def log_2(a: int) -> int: 
    assert a >= 1
    count = 0
    while (a > 1):
        a = a // 2
        count += 1
    return count

def int_to_binary_rep(a: int) -> str:
    """
    https://www.geeksforgeeks.org/problems/binary-representation5003/1
    """

    if a == 0:
        return '0'

    res = ""
    n = log_2(a)
    for i in range(n, -1, -1):
        bit = a // (2 ** i)
        a = a - bit * (2 ** i)
        res	+= str(bit)

    # append '32 - n' zeros
    return '0' * (29 - n) + res


def setBits(a: int) -> int:
    """
    https://www.geeksforgeeks.org/problems/set-bits0143/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article    
    """

    if a == 0:
        return 0
    
    count = 0
    n = log_2(a)
    for i in range(n, -1, -1):
        bit = a // (2 ** i)
        a = a - bit * (2 ** i)
        count += (bit == 1)
    
    return count


def addBinary(binary_rep1: str, binary_rep2: str) -> str:
    # make sure to trim any extra 0s upfront
    if len(binary_rep1) > 1:
        index1 = binary_rep1.find('1')
        binary_rep1 = binary_rep1[index1:]
            
    if len(binary_rep2) > 1:
        index1 = binary_rep2.find('1')
        binary_rep2 = binary_rep2[index1:]
        
    # first align the lengths
    min_s, max_s = sorted([binary_rep1, binary_rep2], key=len)
    # append so the lengths are the same
    min_s = '0' * (len(max_s) - len(min_s)) + min_s

    assert len(min_s) == len(max_s)
    n = len(max_s)
    res = list('0' * n)
    comp = 0
    for i in range(n - 1, -1, -1):
        add_res = int(min_s[i]) + int(max_s[i]) + comp
        res[i:i + 1] = str(add_res % 2)
        comp = int(add_res >= 2)
    

    if comp == 1:
        res = ['1'] + res

    return "".join(res)

if __name__ == '__main__':  
    # for i in range(1, 1000):
    #     bin_i = int_to_binary_rep(i)
    #     for j in range(1, 1000):
    #         bin_j = int_to_binary_rep(j)
    #         bin_res = addBinary(bin_i, bin_j)
    #         res = i + j
    #         assert bin_res == int_to_binary_rep(res)            
    
    s1 = '000'
    s2 = '0001'
    print(addBinary(s1, s2))
