# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "learnCppTutorials/functions.h"
# include "oop/more_inheritance.h"
# include "CustomDS/data_structures/DLL.h"
# include <utility>
# include "CustomDS/iterators/iterators.h"
# include "CustomDS/algorithms/search.h"

void oop_custom_containers();
void arrayListFunction();
void dll_function();
void test_bst();
void play_with_iterators();

void custom_ds_algo_iterator() {
    DoubleLinkedList<double> list {};
    for (int i = 0; i < 5; i++) {
        list.add(i);
    }
    std::cout << "The list: "<< list << "\n";


    //    MutableDLLIterator<double> being = list.end();
    DLLNode<double> node{12};
    DLLNode<double> anotherNode {node};
    anotherNode = node;
    MutableDLLIterator<double> iterator {node};

    //    std::cout << node.val  << " " << node.next << " " << node.previous << "\n";
//    std::cout << anotherNode.val  << " " << anotherNode.next << " " << anotherNode.previous << "\n";
}


int main() {
//game();
//dll_function();
//array_function();
//arrayListFunction();
//oop_custom_containers();
//some_function();
//unique_pointers();

//auto increment = [] (int x) -> int {return x + 1;};
//
//play_with_iterators();

custom_ds_algo_iterator();
}

