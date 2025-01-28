import os
import math

def is_prime(n: int) -> bool:
    if n < 1:
        return False
    
    if n == 2:
        return True
    
    if n % 2 == 0:
        return False

    sqrt_n = int(math.ceil(math.sqrt(n)))

    for divisor in range(3, sqrt_n + 1, 2):
        if n % divisor == 0:
            return False

    return True


def find_primes(n: int):
    return [k for k in range(2, n + 1) if is_prime(k)]


