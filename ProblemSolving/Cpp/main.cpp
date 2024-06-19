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
    n1.right = &n7;

    n2.left = &n3;
    n2.right = &n4;

    n4.left = &n5;
    n4.right = &n6;

    n7.right = &n8;

    n8.right = &n9;

    n9.left = &n11;
    n9.right = &n10;

    n11.left = &n12;
    n11.right = &n13;

    n9.right = &n10;

//    n3.left = &n5;
//    n5.left = &n8;
//
//    n2.right = &n4;
//    n4.left = &n6;
//    n6.left = &n7;

    auto res = depth_and_diameter(&n1);

    std::cout << "depth " << res.first << " diameter " << res.second << "\n";
}

int main() {
    trees_f();
}
