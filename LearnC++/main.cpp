# include <vector>
# include <string>
# include <bits/stdc++.h>
# include <algorithm>
# include "header.h" // this is how we include custom header files
# include "DataStructures/linked_list.h"

int main() {
//    std::vector<int> v1 {4, 2, -4, 10, 23, 0, -5};
//    std::vector<int> v2 {1, 2, 5, 3};
//    std::vector<int> v1_sorted = merge_sort(v1);
//    std::vector<int> v2_sorted = merge_sort(v2);
//    print_vector(v1_sorted);
//    print_vector(v2_sorted);

    // setting the initial head
    Node* head = new Node();
    head -> data = 1;
    head -> next = nullptr;

    for (int i = 2; i <= 4; i ++) {
        head = insert_element(head, i);
    }
    print_linked_list(head);

    std::cout << std:: boolalpha << hasCycle(head) << "\n";

    // let's create a cyclic linked list
    Node* n1 = new Node();
    n1->data = 1;

    Node* n2 = new Node();
    n2->data = 2;

    Node* n3 = new Node();
    n3->data = 3;

    n1 -> next = n2;
    n2 -> next = n3;
    n3 -> next = n2;

    std::cout << std::boolalpha << hasCycle(n1) << "\n";
}

