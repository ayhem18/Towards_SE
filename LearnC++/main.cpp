# include <algorithm>
# include "containers.h"
# include "DataStructures/BST.h"
# include "oop/oop_starter.h"
# include "oop/oop_inheritance.h"
# include "learnCppTutorials/functions.h"
# include "learnCppTutorials/compond_types.h"

int getInteger() {
    return 0;
}

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

void play_with_fruits() {
    const Apple a{ "Red delicious", "red", 4.2 };
    const Banana b{ "Cavendish", "yellow" };
    const Fruit f {"fruit", "green"};
    b.f();
}

void function_overloading() {
    functionWithNumbers(10); // int
    functionWithNumbers(10.0f); // float
//    functionWithNumbers(10.0); // double
    functionWithNumbers(true); // type expansion
    functionWithNumbers('a'); // int: type conversion
//    functionWithNumbers("Ayhem"); compilation error no match

}

int main() {
    pointers_stuff();
}
