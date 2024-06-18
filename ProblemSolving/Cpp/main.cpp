#include <iostream>
# include "arrays/searching.h"
# include "arrays/prefixSum.h"
# include "trees/file1.h"


void trees_f() {
    Node n1(1);
    Node n2(2);
    Node n3(3);
    Node n4(4);
    Node n5(5);
    Node n6(6);
    Node n7(7);
    Node n8(8);
    Node n9(9);

    n1.right = &n2;

    auto res = boundary(&n1);

    for (int v: res) {
        std::cout << v << " ";
    }
    std::cout << "\n";
}

int main() {
    trees_f();
}
