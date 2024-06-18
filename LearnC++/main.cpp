# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "learnCppTutorials/functions.h"
# include "oop/more_inheritance.h"
# include "CustomDS/data_structures/linear/DLL.h"
# include "CustomDS/data_structures/trees/binaryTree.h"
# include "CustomDS/algorithms/search.h"

void oop_custom_containers();
void arrayListFunction();
void dll_function();
void test_bst();
void play_with_iterators();

void custom_ds_algo_iterator() {
    DoubleLinkedList<double> list {};
    for (int i = 0; i < 5; i++) {
        list.add(1);
    }
    for (int i = 5; i >= 0; i--) {
        list.add(i);
    }
    std::cout << "The list: "<< list << "\n";

    for (int i = 0; i <= 5; i++) {
        // define the 'begin' and 'end' iterators for each use
        auto begin = list.begin();
        auto end = list.end();
        int c = count(begin, end, i);
        std::cout << i << " appears "<< c << " times in the list" << "\n";
    }
}

void customBinaryTree() {
    BinaryTree<double> tree;
    for (int i = 0; i < 4; i ++) {
        tree.add(i);
    }
    std::cout << tree << "\n";
}

# include "ProblemSolving/DivideAndConquer/problems_set1.h"
# include "ProblemSolving/graph/basics.h"

void graph_f() {
    std::cout << maxWeightCell(3, {2, 0, -1, 2}) << "\n";
}

int main() {
    graph_f();
}

