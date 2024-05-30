# include "list.h"
# include <cassert>
# include <string>

//// let's add some elements:

// let's delete some items
//template <typename T>
//void DoubleLinkedList<T>::remove(const T& val) {
//    // if the list is empty:
//    if (this -> m_size == 0) {
//        return;
//    }
//    if ((this -> m_size == 1) && (head -> val == val)) {
//        // at this point
//        head = nullptr;
//        tail = nullptr;
//        this -> m_size = 0;
//    }
//    // we have at least 2 elements in the list: head and tail are supposedly different
//    DLLNode<T>* traverse_node = head;
//    while ((traverse_node != nullptr) && (traverse_node -> val != val)) {
//        traverse_node  = traverse_node -> next;
//    }
//    if (traverse_node == nullptr) {
//        // the element to be removed was not found here, abort
//        return;
//    }
//
//    // at this point, we know the element was found
//    // reduce the size
//    this -> size --;
//    // 2 operations to be done: for the next of traverse node: set the 'previous'
//    // for the 'previous' of traverse_node set the 'next'
//    DLLNode<T>* prev = traverse_node -> previous;
//    DLLNode<T>* next = traverse_node -> next;
//
//    // 2 things can go wrong here: previous is null: meaning, we are dealing with the head
//    if (prev == nullptr) {
//        head = next;
//        free(traverse_node);
//        return;
//    }
//
//    // if next is null, then we are dealing with the tail of the list
//    if (next == nullptr) {
//        // the 'prev' node should point to null now
//        prev -> next = nullptr;
//        tail = prev;
//        free(traverse_node);
//        return;
//    }
//
//    // we are neither at the head nor the tail
//    prev -> next = next;
//    next -> previous = prev;
//    free(traverse_node);
//}


//template <typename T>
//void DoubleLinkedList<T>::addAt(const T& val, int index) {
//    // the index cannot be larger than the current size or less than 0
//    assert((index >= 0) && (index <= this -> m_size) &&
//    "the index should be larger than 0 and less than " + static_cast<std::string>(this -> m_size) + ". Found " + static_cast<std::string>(this -> index));
//
//
//    // create the new node
//    auto* new_node = new DLLNode<T> {val};
//
//    // consider the case of the head
//    if (index == 0) {
//        // set the next pointer to the current head
//        new_node -> next = this -> head;
//        this -> head -> previous = new_node;
//        // set the head to the new node
//        this -> head = new_node;
//        // increase the size
//        this -> m_size += 1;
//
//        return;
//    }
//
//    DLLNode<T> traverse_node = this -> head;
//    int count = 0;
//    while (count < index - 1) {
//        count ++;
//        traverse_node = traverse_node -> next;
//    }
//    // at this point the 'traverse_node' is at the 'index - 1' position.
//    new_node -> next = traverse_node -> next;
//    new_node -> previous = traverse_node;
//
//    traverse_node -> next -> previous = new_node;
//    traverse_node -> next = new_node;
//
//    if (index == this -> m_size) {
//        // modify the tail if the element is added to the end of the list
//        this -> tail = new_node;
//    }
//
//    // increase the size
//    this -> m_size += 1;
//}

//template <typename T>
//void DoubleLinkedList<T>:: removeAt(int index) {
//    // the index cannot be larger than the current size or less than 0
//    assert((index >= 0) && (index < this -> m_size) &&
//           "the index should be larger than 0 and less than " + static_cast<std::string>(this -> m_size) + ". Found " + static_cast<std::string>(this -> index));
//
//    // consider the case of the head
//    if (index == 0) {
//        DLLNode<T> new_head = (this -> head) -> next;
//        new_head -> previous = nullptr;
//        // free the previous head
//        free(this -> head);
//        this -> head = new_head;
//
//        // decrease the size
//        this -> m_size -= 1;
//
//        return;
//    }
//    // let's consider other cases
//    auto traverse_node = this -> head;
//
//    int count = 0;
//    while (count < index - 1) {
//        count ++;
//        traverse_node = traverse_node -> next;
//    }
//
//    // at this point the 'traverse_node' is at the 'index - 1' position
//    DLLNode<T> new_next_node = traverse_node -> next -> next;
//    new_next_node -> previous = traverse_node;
//    free(traverse_node -> next);
//    traverse_node -> next = new_next_node;
//
//    if (index == this -> m_size - 1) {
//        // modify the tail if the element is added to the end of the list
//        this -> tail = traverse_node;
//    }
//
//    // decrease the size
//    this -> m_size -= 1;
//}

