#include <iostream>
# include "arrays/searching.h"
# include "arrays/prefixSum.h"

void f() {
    int n = 7;
    int a [] =  {-2, 2, -5, 12, -11, -1, 7};
    std::cout << longSubarrWthSumDivByK(a, 7, 3)  << "\n";

}

int main() {
    f();
}
