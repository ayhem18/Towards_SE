#ifndef LEARNC___DLL_H
#define LEARNC___DLL_H

// let's start with a fast implementation of the array List

#include <cstdlib>
#include <iostream>
# include "list.h"

template <typename T>
class DLLNode {
public:
    T val;
    DLLNode<T> *next {nullptr};
    DLLNode<T> *previous {nullptr};
    DLLNode(T val, DLLNode* n, DLLNode*prev): val{val}, next{n}, previous{prev} {};
    // calling the 3 argument constructor
    // either specify both next and previous nodes or none of them
    explicit DLLNode(T val): DLLNode(val, nullptr, nullptr) {};
};


template <typename T>
class DoubleLinkedList: public List<T> {
private:
    // the head
    DLLNode<T>* head {nullptr};
    // the tail
    DLLNode<T>* tail {nullptr};

public:
    explicit DoubleLinkedList(T val):
            List<T>(1), head{nullptr}, tail{nullptr} {
        this -> head = new DLLNode(val);
        this -> tail = head;
    }
    DoubleLinkedList():List<T>{}, head{nullptr}, tail{nullptr} {};

    // let's create the destructor
    ~DoubleLinkedList() {
        // create some traverse node
        DLLNode<T>* traverse_node = head;
        while (traverse_node != nullptr) {
            DLLNode<T>* next = traverse_node -> next;
            free(traverse_node);
            traverse_node = next;
        }
    }

    void add(const T& val) override;

    void remove(const T& val) override;

    void addAt(const T& val, int index) override;

    void removeAt(int index) override;

    // let's create a friend function to display the content of the linked list
    friend std::ostream& operator <<(std::ostream& out, const DoubleLinkedList<T>& list){
        if (list.size() == 0) {
            out << "The list is empty";
            return out;
        }

        DLLNode<T>* traverse_node = list.head;
        // first display the value at the head
        out << traverse_node -> val;
        traverse_node = traverse_node -> next;
        while (traverse_node != nullptr) {
            out << "-->" << traverse_node -> val;
            traverse_node = traverse_node -> next;
        }
        return out;
    };
};

// member functions definitions

template<typename T>
void DoubleLinkedList<T>::add(const T& val) {
    // start with the simple case, if the list is empty
    if (this -> m_size == 0) {
    this -> head = new DLLNode<T>(val);
    this -> tail = head;
    }

    // if there is only one element
    else if (this -> m_size == 1) {
    auto * new_node = new DLLNode<T>(val, nullptr,  head);
    head -> next = new_node;
    tail = new_node;
    }

    else {
    // create a new node
    auto * new_node = new DLLNode<T>(val, nullptr,  tail);
    // link the tail to the new node
    tail -> next = new_node;
    tail = new_node;
    }

    // regardless increase the size
    this -> m_size += 1;
}

template <typename T>
void DoubleLinkedList<T>::remove(const T &val) {
    // if the list is empty:
    if (this->m_size == 0) {
        return;
    }
    if ((this->m_size == 1) && (head->val == val)) {
        // free the memory allocated by the head
        free(head);
        head = nullptr;
        tail = nullptr;
        this->m_size = 0;
    }
    // we have at least 2 elements in the list: head and tail are supposedly different
    DLLNode<T>* traverse_node = head;
    while ((traverse_node != nullptr) && (traverse_node->val != val)) {
        traverse_node = traverse_node->next;
    }

    if (traverse_node == nullptr) {
        // the element to be removed was not found here, abort
        return;
    }

    // at this point, we know the element was found
    // reduce the size
    this-> m_size--;

    // 2 operations to be done: for the next of traverse node: set the 'previous'
    // for the 'previous' of traverse_node set the 'next'
    DLLNode<T>* prev = traverse_node->previous;
    DLLNode<T>* next = traverse_node->next;

    if (prev == nullptr) {
        // if previous is nullptr, that means that traverse_node is the head
        next -> previous = nullptr;
        head = next;
        free(traverse_node);
        return;
    }
//
    // if next is null, then we are dealing with the tail of the list
    if (next == nullptr) {
        // the 'prev' node should point to null now
        prev->next = nullptr;
        tail = prev;
        free(traverse_node);
        return;
    }

    // we are neither at the head nor the tail
    prev-> next = next;
    next-> previous = prev;
    free(traverse_node);
}

template <typename T>
void DoubleLinkedList<T>::addAt(const T &val, int index) {
    // the index cannot be larger than the current size or less than 0
    assert((index >= 0) && (index <= this -> m_size) && "the index should be larger than 0 and less or equal to the size of the list");

    // create the new node
    auto new_node = new DLLNode<T> {val};

    // consider the case of the head
    if (index == 0) {
        // let's consider the case where the list is empty
        if (this -> m_size == 0) {
            this -> head = new_node;
            this -> tail = new_node;
            this -> m_size ++;
            return;
        }

        // set the next pointer to the current head
        new_node -> next = this -> head;
        this -> head -> previous = new_node;
        // set the head to the new node
        this -> head = new_node;
        // increase the size
        this -> m_size += 1;
        return;
    }
//
    DLLNode<T>* traverse_node = this -> head;
    int count = 0;
    while (count < index - 1) {
        count ++;
        traverse_node = traverse_node -> next;
    }

//
    // at this point the 'traverse_node' is at the 'index - 1' position.
    new_node -> next = traverse_node -> next;
    new_node -> previous = traverse_node;

    // we will first consider the case of the tail
    if (index == this -> m_size) {
        // modify the tail if the element is added to the end of the list
        traverse_node -> next = new_node;
        this -> tail = new_node;
        this ->  m_size += 1;
        return;
    }

    // at this point we know that traverse_node -> next is different from null
    traverse_node -> next -> previous = new_node;
    traverse_node -> next = new_node;

    // increase the size
    this -> m_size += 1;
}

template<typename T>
void DoubleLinkedList<T>::removeAt(int index) {
    // the index cannot be larger than the current size or less than 0
    assert((index >= 0) && (index < this -> m_size) && "the index should be larger than 0 and less than the size of the list");

    if (this -> m_size == 0) {
        return;
    }
    // consider the case of the head
    if (index == 0) {
        if (this -> m_size == 1) {
            free(this -> head);
            this -> head = nullptr;
            this -> tail = nullptr;

            this -> m_size --;
            return;
        }
        // at this point we know that this -> head -> next
        // is not null
        auto new_head = (this -> head) -> next;
        new_head -> previous = nullptr;
        // free the previous head
        free(this -> head);
        this -> head = new_head;
        this -> m_size --;
        return;
    }
    // let's consider other cases
    auto traverse_node = this -> head;

    int count = 0;
    while (count < index - 1) {
        count ++;
        traverse_node = traverse_node -> next;
    }

    // at this point the 'traverse_node' is at the 'index - 1' position
    if (index == this -> m_size - 1) {
        // it means we are removing the last element of the list
        // free the last element
        free(traverse_node -> next);
        // set it to nullptr
        traverse_node -> next = nullptr;
        // set the tail to the traverse node
        this -> tail = traverse_node;
        this -> m_size --;
        return;
    }
    this -> m_size --;

    // at this point we know that 'traverse -> next -> next' is not null
    DLLNode<T>* new_next_node = traverse_node -> next -> next;
    // link the new next node to the traverse node
    new_next_node -> previous = traverse_node;

    free(traverse_node -> next);
    traverse_node -> next = new_next_node;
}



#endif //LEARNC___DLL_H
