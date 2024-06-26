#ifndef LEARNC___DLL_H
#define LEARNC___DLL_H

// let's start with a fast implementation of the array List
#include <cstdlib>
#include <iostream>
#include "list.h"
#include "../../iterators/iterators.h"
#include <typeinfo>

template <typename T>
class DLLNode {
public:
    T val;
    DLLNode<T> *next {nullptr};
    DLLNode<T> *previous {nullptr};

    // initialize the field 'val' to the default value of type T and null pointers to 'next' and 'previous' fields
    DLLNode() = default;

    DLLNode(T val, DLLNode* n, DLLNode*prev): val{val}, next{n}, previous{prev} {};
    // calling the 3 argument constructor
    // either specify both next and previous nodes or none of them
    explicit DLLNode(T val): DLLNode(val, nullptr, nullptr) {};

//     copy constructor
    DLLNode(const DLLNode& another): DLLNode(another.val, another.next, another.previous) {};

//    DLLNode& operator = (const DLLNode<T>& another) {
//        if (another == *this){
//            return *this;
//        }
//        val = another.val;
//        next = another.next;
//        previous = another.previous;
//        return *this;
//    }

    bool operator == ( const DLLNode<T>& another_node) const {
        return val == another_node.val && next == another_node.next && previous == another_node.previous;
    }

};


/////////////////////////////////// forward Declaration of the iterator ///////////////////////////////////
template <typename T>
class MutableDLLIterator: public MutableBiDirIterator<T> {
private:
    DLLNode<T>* m_node;
public:
    MutableDLLIterator() = default;
    explicit MutableDLLIterator(DLLNode<T>* node): m_node(node) {};
    // override the * operator
    T& operator * () {
        return m_node -> val;
    }
//

    bool operator != (const MutableIterator<T>& another) override{
        // first check for the type
        if (typeid(another) != typeid(*this)){
            return true;
        }

        // return true;

        auto final_another = dynamic_cast<const MutableDLLIterator*>(&another);
        return m_node != final_another -> m_node;
    }

    bool operator == (const MutableIterator<T>& another) {
        // first check for the type
        if (typeid(another) != typeid(*this)){
            return false;
        }
//        return true;
//        // at this point of the code,  another can be cast to MutableDLLIterator
        auto final_another = dynamic_cast<const MutableDLLIterator*>(&another);
        return m_node == final_another -> m_node;
    }
//
    MutableDLLIterator& operator = (const MutableDLLIterator& another) {
        m_node = another -> m_node;
        return *this;
    }

    MutableDLLIterator<T>& operator ++ (int) override{
        m_node = m_node -> next;
        return *this;
    }
//
    MutableDLLIterator<T>& operator -- (int)  override {
        m_node = m_node -> previous;
        return *this;
    }
};

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
template <typename T>
class DoubleLinkedList: public List<T> {
private:
    // the head
    DLLNode<T>* head {nullptr};
    // the tail
    DLLNode<T>* tail {nullptr};
    // the sentinel node: represents the end of the linked list
    DLLNode<T>* sentinel {nullptr};
public:
    explicit DoubleLinkedList(T val):
            List<T>(1), head{nullptr}, tail{nullptr}, sentinel{nullptr}{
        this -> head = new DLLNode<T>(val);
        this -> tail = head;
        this -> sentinel = new DLLNode<T>();
    }
    DoubleLinkedList():List<T>{}, head{nullptr}, tail{nullptr} {};

    // let's create the destructor
    ~DoubleLinkedList() {
        std::cout << "\ncalling the DLL destructor\n";
        // create some traverse node
        DLLNode<T>* traverse_node = head;
        while (traverse_node != nullptr) {
            DLLNode<T>* next = traverse_node -> next;
            delete traverse_node;
            traverse_node = next;
        }
    }

    void add(const T& val) override;

    void remove(const T& val) override;

    void addAt(const T& val, int index) override;

    void removeAt(int index) override;

    T get (int index) const override;

    // let's create a friend function to display the content of the linked list
    friend std::ostream& operator << (std::ostream& out, const DoubleLinkedList<T>& list) {
//        out << "\n the DLL implementation of <<\n";
        if (list.size() == 0) {
            out << "The list is empty";
            return out;
        }

        DLLNode<T>* traverse_node = list.head;
        // first display the value at the head
        out << traverse_node -> val;
        traverse_node = traverse_node -> next;
        while (traverse_node != list.sentinel) {
            out << " --> " << traverse_node -> val;
            traverse_node = traverse_node -> next;
        }
        return out;
    };
    // adding the iterator as a friend class
    friend class MutableDLLIterator<T>;

    // create a function to get the head iterator
    MutableDLLIterator<T> begin() {
        // make sure to return the sentinel node if the list is empty
        if (this -> m_size == 0) {
            return MutableDLLIterator<T>(sentinel);
        }
        return MutableDLLIterator<T>(head);
    }

    MutableDLLIterator<T> end() {
        // this is always a valid call since the sentinel field is never set as to 'nullptr'
        return MutableDLLIterator<T>(sentinel);
    }
};

template<typename T>
void DoubleLinkedList<T>::add(const T& val) {
    // start with the simple case, if the list is empty
    if (this -> m_size == 0) {
        this -> head = new DLLNode<T>(val);
        this -> tail = head;
        this -> sentinel = new DLLNode<T>();
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

    tail -> next = sentinel;
    // make sure to link the tail to the sentinel node
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
        delete head;
        head = nullptr;
        tail = nullptr;
        this->m_size = 0;
        return;
    }
    // we have at least 2 elements in the list: head and tail are supposedly different
    DLLNode<T>* traverse_node = head;
    while ((traverse_node != sentinel) && (traverse_node->val != val)) {
        traverse_node = traverse_node->next;
    }

    if (traverse_node == sentinel) {
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
        delete traverse_node;
        return;
    }
//
    // if next is null, then we are dealing with the tail of the list
    if (next == sentinel) {
        // the 'prev' node should point to null now
        prev->next = sentinel;
        tail = prev;
        delete traverse_node;
        return;
    }

    // we are neither at the head nor the tail
    prev-> next = next;
    next-> previous = prev;
    delete traverse_node;
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
            tail -> next = sentinel;
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
        this -> tail -> next = sentinel;
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
        delete traverse_node -> next;
        // set it to sentinel
        traverse_node -> next = sentinel;
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

    delete traverse_node -> next;
    traverse_node -> next = new_next_node;
}

template <typename T>
T DoubleLinkedList<T>::get(int index) const {
    // make sure to check the index range
    assert((index >= 0) && (index < this -> m_size) && "the index should be larger than 0 and less or equal to the size of the list");
    std::cout << "\nThe DoublyLinkedList class calling the 'get' function with index " << index << "\n";
    DLLNode<T>* traverse_node = this -> head;
    int count = 0;
    while (count < index) {
        count ++;
        traverse_node = traverse_node -> next;
    }
    return traverse_node -> val;
}

#endif //LEARNC___DLL_H
