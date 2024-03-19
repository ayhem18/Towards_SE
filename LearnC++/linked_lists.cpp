# include <iostream>
// Definition for singly-linked list.

struct ListNode {
      int val;
      ListNode *next;
};


// what's wrong with code ???
// the local object is not returned due to move semantics

//ListNode insert_element(ListNode* head, int value) {
//    // this function will insert the new value at the beginning of the linked list
//    // and return the new head object
//    ListNode new_head {value, head};
//    return new_head;
//}

ListNode* insert_element(ListNode * head, int value) {
    // allocate the
    ListNode* new_head = new ListNode();
    // this code was found on GeeksForGeeks Insertion to linked list
    new_head -> val = value;
    // same as (*new_head).val = value
    (*new_head).next = head;
    return new_head;
}

void print_linked_list(ListNode* head) {
    if (head == nullptr) {
        std::cout << "The list is empty" << '\n';
        return;
    }
    ListNode traverse_node{*head};
    std::cout << traverse_node.val;
    while (traverse_node.next != nullptr) {
        std::cout << "-->";
        traverse_node = *(traverse_node.next);
        std::cout << traverse_node.val;
    }
    // add a small new line character in the end
    std::cout << "\n";
}

bool hasCycle(ListNode *head) {
    // let's
    if (head == nullptr || head->next == nullptr) {
        return false;
    }
    // at this point we know that the linked list has at least 2 elements
    // we will create 2 pointers, one usual traversing node, another that traverses 2 nodes at a time
    ListNode* pt1 = head;
    ListNode* pt2 = head;
    while (true) {
        // move pt1
        if (pt1->next == nullptr) {
            return false;
        }
        pt1 = pt1 -> next;

        // move pt2
        if (pt2 -> next == nullptr) {
            return false;
        }
        pt2 = pt2 -> next;

        if (pt2 -> next == nullptr) {
            return false;
        }
        pt2 = pt2 -> next;

        // at this point check if pt2 and pt1 are the same
        if (pt1 == pt2) {
            return true;
        }
    }
}

struct Node
{
    int data;
    struct Node *next;
};

void printList(struct Node *head)
{
    // this function assumes the linked list is circular
    if (head == nullptr) {
        std:: cout << "the list is empty"  << "\n";
        return;
    }
    // display the content of the head
    std::cout << head -> data << " ";
    Node* traverse_node = head -> next;
    while (traverse_node != head) {
        std::cout << traverse_node -> data << " ";
        traverse_node = traverse_node -> next;
    }
}
