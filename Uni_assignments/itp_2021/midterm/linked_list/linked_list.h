// this header contains the implementation of a general linked list
#ifndef LEARNC___LINKED_LIST_H
#define LEARNC___LINKED_LIST_H

# include <iostream>
# include <cassert>

template <typename T>
class LinkedListNode {
private:
    T data;
    LinkedListNode* next;
public:
    LinkedListNode(T data, LinkedListNode* next): data(data) {
        this-> next = next;
    };
    explicit LinkedListNode(T data): LinkedListNode(data, nullptr) {};
};

template <typename T>
class LinkedList {
private:
    int size {0};
    LinkedListNode<T>* head = nullptr;
public:
//    LinkedList() = default;
    explicit LinkedList(T val): size{0}
    {
        // set the head with the new keyword
        head = new LinkedListNode(val, nullptr);
    };

    ~LinkedList()
    {
        // the main goal of the destructor is to clear the memory occupied by the linked list
        LinkedList* traverse_node = this -> head;
        while (traverse_node != nullptr) {
            LinkedList* next = traverse_node -> next;
            free(traverse_node);
            traverse_node = next;
        }
        std::cout << "The memory allocated by the linked list has been completely cleared !!\n";
    }


    // add an element to the linked list
    void add_element(T data) {
        // create the new node
        LinkedList<T>*  newNode = new LinkedList (data, head);
        this -> head = newNode;
        // increment the size
        this -> size ++;
    }

    void add_element(T data, int index) {
        // make sure the index is in the correct range
        assert((index >= 0) && (index <= this -> size));
        if (index == 0) {
            return this -> add_element(data);
        }

        int count = 0;
        LinkedList<T>* traverse_node = head;
        while (count != index - 1) {
            traverse_node = traverse_node -> next;
            count += 1;
        }
        // create the new node
        LinkedList<T> new_node = new LinkedList(data, traverse_node -> next);
        traverse_node -> next = new_node;
        this -> size ++;
    }

    void print() const {
        if (head == nullptr) {
            std::cout << "The linked list is empty\n";
            return;
        }
        LinkedList<T> traverse_node = head;
        std:: cout << head -> data;
        traverse_node = traverse_node -> next;
        while (traverse_node != nullptr) {
            std:: cout << " --> " << traverse_node -> data;
            traverse_node = traverse_node -> next;
        }
    }

};


#endif //LEARNC___LINKED_LIST_H
