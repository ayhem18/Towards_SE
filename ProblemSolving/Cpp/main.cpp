#include <iostream>
# include "arrays/searching.h"
# include "arrays/prefixSum.h"
# include "twoPointers/file1.h"

void negNumbers() {
    long long int A[] = {-1, -2, 1, -4, -5};
    int K = 1;
    for (int k = 1; k <= 5; k++) {
        auto res = printFirstNegativeInteger(A, 5, k);

        std:: cout << "K: " << k << "\n";
        for (auto& v: res) {
            std::cout << v << " ";
        }
        std::cout << "\n";
    }
}

int main() {
    negNumbers();
}
