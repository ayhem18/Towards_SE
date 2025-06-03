# include <stdbool.h>

bool is_prime(int n) {
    if (n <= 1) {
        return false;
    }

    if (n == 2) {
        return true;
    }

    // at this point n > 2, which means any even number if not prime
    if (n % 2 == 0) {
        return false;
    }

    // ignore all even possible divisors
    
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}