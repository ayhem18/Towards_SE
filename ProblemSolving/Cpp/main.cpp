#include <iostream>
# include "arrays/searching.h"

int main() {
    int a1[] ={5, 10, 20, 40} ;
    std::vector<int> c = leaders(4, a1);

    for (int & v: c) {
        std::cout << v << " ";
    }
    std::cout << "\n";
}
