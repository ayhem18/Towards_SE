# include <algorithm>
# include "DataStructures/BST.h"
# include "containers.h"
# include "oop/oop_starter.h"
//# include "oop/oop_starter.cpp"

int getInteger();

int mod(int x, int y) {
    return ((x % y) + y) % y;
}

int getInteger();

void test_bst(){
    Node* n20 = new Node(20);
    Node* n10 = insertNode(n20, 10);
    Node* n27 = insertNode(n20, 27);
    Node* n25 = insertNode(n10, 15);
    Node* n5 = insertNode(n10, 5);
    Node* n22 = insertNode(n27, 22);

    inorderTraversal(n20);

    for (int i = 0; i < 10; i ++ ){
        int x = getInteger();
        n20 = deleteNode(n20, x);
        std::cout << "\nafter deleting " << x << '\n';
        inorderTraversal(n20);
    }
//

    freeBSTMemory(n20);
}
Ball f() {
    return Ball(1, "color");
}

int main() {
//    Ball def{};
//    Ball blue{ "blue" };
//    Ball twenty{ 20.0 };
//    Ball blueTwenty{ "blue", 20.0 };
    Ball b1 {}; // won't display anythin
    // will display the copy constructor once
    Ball b2 {b1};
    // each of them will display the copy constructor
    // and then the print statement defined in the function body
    print_ball(b1);
    print_ball(b2);
}
