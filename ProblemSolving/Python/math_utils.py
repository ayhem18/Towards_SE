"""
This script contains my implementation of basic Mathematical algorithms: Mainly number theory
"""


def greatest_common_divisor(a: int, b: int) -> int:
    # make sure the arguments are integer
    if not (isinstance(a, int) and isinstance(b, int)):
        raise TypeError("Make sure the arguments are INTEGERS !!")
    
    a, b = abs(a), abs(b)

    maximum, minimum = max(a, b), min(a, b)

    if minimum == 0:
        return maximum
    
    return greatest_common_divisor(maximum % minimum, minimum)