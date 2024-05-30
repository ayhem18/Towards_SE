# include "dll.h"

// let's add some elements:
//void DoubleLinkedList::add(const int& val) {
//    // start with the simple case, if the list is empty
//    if (this -> size == 0) {
//        this -> head = new DLLNode(val);
//        this -> tail = head;
//    }
//
//    // if there is only one element
//    else if (this -> size == 1) {
//        DLLNode* new_node = new DLLNode(val, nullptr,  head);
//        head -> next = new_node;
//        tail = new_node;
//    }
//
//    else {
//        // create a new node
//        DLLNode* new_node = new DLLNode(val, nullptr,  tail);
//        // link the tail to the new node
//        tail -> next = new_node;
//        tail = new_node;
//    }
//
//    // regardless increase the size
//    this -> size += 1;
//}
//
//// let's delete some items
//void DoubleLinkedList::remove(const int& val) {
//    // if the list is empty:
//    if (size == 0) {
//        return;
//    }
//    if ((size == 1) && (head -> val == val)) {
//        // at this point
//        head = nullptr;
//        tail = nullptr;
//        size = 0;
//    }
//    // we have at least 2 elements in the list: head and tail are supposedly different
//    DLLNode* traverse_node = head;
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
//    size --;
//    // 2 operations to be done: for the next of traverse node: set the 'previous'
//    // for the 'previous' of traverse_node set the 'next'
//    DLLNode* prev = traverse_node -> previous;
//    DLLNode* next = traverse_node -> next;
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
//
//
//// let's implement the print functionality
//std::ostream& operator<< (std::ostream& out, const DoubleLinkedList& list) {
//    // let's start with the head
//    if (list.size == 0) {
//        out << "The list is empty";
//        return out;
//    }
//
//    DLLNode* traverse_node = list.head;
//    // first display the value at the head
//    out << traverse_node -> val;
//    traverse_node = traverse_node -> next;
//    while (traverse_node != nullptr) {
//        out << "-->" << traverse_node -> val;
//        traverse_node = traverse_node -> next;
//    }
//    return out;
//}
