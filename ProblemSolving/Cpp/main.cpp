#include <iostream>
# include "arrays/searching.h"
# include "arrays/prefixSum.h"
# include "twoPointers/file1.h"
void f() {
    int n = 7;
    int a [] =  {-2, 2, -5, 12, -11, -1, 7};
    std::cout << longSubarrWthSumDivByK(a, 7, 3)  << "\n";

}

void loopLinkedList() {

    Node n5 = Node(5);
    Node n4 = Node(4);
    n4.next = &n5;
    Node n3 = Node(2);
    n3.next = &n4;
    Node n2 = Node(3);
    n2.next = &n3;
    Node n1 = Node(1);
    n1.next = &n2;

    n5.next = &n5;
    int v = findFirstNode(&n1);
    std::cout << v << "\n";
}

int main() {
    loopLinkedList();
}
