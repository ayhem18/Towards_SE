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
    Node n10(10);
    Node n11(11);
    Node n12(12);
    Node n13(13);

    n1.left = &n2;
    n1.right = &n3;

    n2.left = &n4;
    n2.right = &n5;

    n3.left = &n6;
    n3.right = &n7;

    n6.left = &n8;
    n6.right = &n9;

    auto res = lca(&n1, 10, 9);

    if (res != nullptr) {
        std::cout << res -> data;
    }
    else {
        std::cout << "no common ancestor";
    }
//    for (int v : res) {
//        std::cout << v << " ";
//    }
    std::cout << "\n";
}

int main() {
    trees_f();
}
