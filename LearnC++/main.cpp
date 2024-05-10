# include <algorithm>
# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "oop/oop_inheritance.h"
# include "learnCppTutorials/functions.h"
# include "CustomDS/dll.h"
# include "oop/oop_more.h"

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

void fractions_and_operators() {
    Fraction f1 {1, 2};
    Fraction f2 {2, 5}; // if b = 0, the code will raise an error
    Fraction f3 {f1 * f2};
    Fraction f4 {f1 * 4};
    std::cout << "f3: " << f3 <<"\n";
    std::cout << "f4: " << f4 <<"\n";
}

void dll_function() {
    DoubleLinkedList l {};
    for (int i = 1; i <= 25 ; i ++) {
        l.add(i);
    }
    int element{0};
    std::cout << "Initial list\n";
    std::cout << "list " << l << "\n";

    while (std::cin >> element) {
        std::cout << "attempting to remove " << element << "\n";
        l.remove(element);
        std::cout << "list " << l << "\n";
    }
}

int main() {
dll_function();
}
