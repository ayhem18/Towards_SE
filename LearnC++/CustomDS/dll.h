#ifndef LEARNC___DLL_H
#define LEARNC___DLL_H

// let's start with a fast implementation of the array List

#include <cstdlib>
#include <iostream>

//class DLLNode {
//public:
//    int val;
//    DLLNode *next {nullptr};
//    DLLNode *previous {nullptr};
//    DLLNode(int val, DLLNode* n, DLLNode*prev): val{val}, next{n}, previous{prev} {};
//    // calling the 3 argument constructor
//    // either specify both next and previous nodes or none of them
//    explicit DLLNode(int val): DLLNode(val, nullptr, nullptr) {};
//
//};


//class DoubleLinkedList {
//private:
//    int size = 0;
//    DLLNode* head {nullptr};
//    DLLNode* tail {nullptr};
//
//public:
//    explicit DoubleLinkedList(int val): size{1}, head{nullptr},tail{nullptr} {
//        this -> head = new DLLNode(val);
//        this -> tail = head;
//    }
//    DoubleLinkedList():size{0}, head{nullptr}, tail{nullptr} {};
//    // let's create the destructor
//    ~DoubleLinkedList() {
//        // create some traverse node
//        DLLNode* traverse_node = head;
//        while (traverse_node != nullptr) {
//            DLLNode* next = traverse_node -> next;
//            free(traverse_node);
//            traverse_node = next;
//        }
//    }
//    // let's add some elements:
//    void add(const int& val);
//    // let's delete some elements
//    void remove(const int& val);
//
//    // let's create a friend function to display the content of the linked list
//    friend std::ostream& operator<< (std::ostream& out, const DoubleLinkedList& list);
//
//};

#endif //LEARNC___DLL_H
