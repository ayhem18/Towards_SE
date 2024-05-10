# include "linked_list.h"
# include <iostream>
// Definition for singly-linked list.


// what's wrong with code ???
// the local object is not returned due to move semantics which messes up the 'next' pointer

//ListNode insert_element(ListNode* head, int value) {
//    // this function will insert the new value at the beginning of the linked list
//    // and return the new head object
//    ListNode new_head {value, head};
//    return new_head;
//}


Node* insert_element(Node * head, int value) {
    // allocate the
    Node* new_head = new Node(value);
    // this code was found on GeeksForGeeks Insertion to linked list
    // same as (*new_head).data = value
    (*new_head).next = head;
    return new_head;
}

void print_linked_list(Node* head) {
    if (head == nullptr) {
        std::cout << "The list is empty" << '\n';
        return;
    }
    Node traverse_node{*head};
    std::cout << traverse_node.data;
    while (traverse_node.next != nullptr) {
        std::cout << "-->";
        traverse_node = *(traverse_node.next);
        std::cout << traverse_node.data;
    }
    // add a small new line character in the end
    std::cout << "\n";
}

bool hasCycle(Node *head) {
    // let's
    if (head == nullptr || head->next == nullptr) {
        return false;
    }
    // at this point we know that the linked list has at least 2 elements
    // we will create 2 pointers, one usual traversing node, another that traverses 2 nodes at a time
    Node* pt1 = head;
    Node* pt2 = head;
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

int countNodesinLoop(struct Node *head)
{
    if (head == nullptr || head->next == nullptr) {
        return false;
    }
    // at this point we know that the linked list has at least 2 elements
    // we will create 2 pointers, one usual traversing node, another that traverses 2 nodes at a time
    Node* pt1 = head;
    Node* pt2 = head;
    while (true) {
        // move pt1
        if (pt1->next == nullptr) {
            return 0;
        }
        pt1 = pt1 -> next;

        // move pt2
        if (pt2 -> next == nullptr) {
            return 0;
        }
        pt2 = pt2 -> next;

        if (pt2 -> next == nullptr) {
            return 0;
        }
        pt2 = pt2 -> next;

        // at this point check if pt2 and pt1 are the same
        if (pt1 == pt2) {
            break;
        }
    }
    // at this point both pt1 and pt2 are pointing to the same node
    int loop_length = 1;
    pt2 = pt2 -> next;
    while (pt2 != pt1) {
        pt2 = pt2 -> next;
        loop_length += 1;
    }
    return loop_length;
}

// this one a bit trickier
// https://www.geeksforgeeks.org/problems/intersection-of-two-sorted-linked-lists/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
Node* findIntersection(Node* head1, Node* head2)
{
    // we know that head1 and head2 represents the heads of sorted linked lists
    Node* new_head{}; // new_head is the nullptr now
    Node* new_tail{};
    Node* traverse1 = head1;
    Node* traverse2 = head2;

    while ( traverse1 != nullptr && traverse2 != nullptr) {
        if (traverse1 -> data == traverse2 -> data) {

            // in case the common list is empty
            if (new_head == nullptr) {
                // allocate new memory
                new_head = new Node(traverse1 -> data);
            }

            // in case the common list has only one element
            else if (new_head -> next == nullptr) {
                // allocate new memory for the tail
                new_tail = new Node(traverse1->data);
                new_head->next = new_tail;
            }

            // in case the common list has at least 2 elements
            else {
                // allocate new node at the new
                Node* new_node = new Node(traverse1 -> data);
                new_tail -> next = new_node;
                new_tail = new_node;
            }

            // don't forget to update both pointers
            traverse1 = traverse1 -> next;
            traverse2 = traverse2 -> next;
        }
        else if ( (traverse1 -> data) > (traverse2 -> data)) {
            traverse2 = traverse2 -> next;
        }
        else {
            traverse1 = traverse1 -> next;
        }
    }

    return new_head;
}


int intersectPoint(Node* head1, Node* head2)
{
    // the first step is to determine whether the linked lists intersect or not
    // while calculating the length of each list
    Node* traverse_node1 = head1;
    Node* traverse_node2 = head2;

    int count1 = 1;
    while (traverse_node1 -> next != nullptr) {
        traverse_node1 = traverse_node1 -> next;
        count1 ++;
    }

    int count2 = 1;
    while (traverse_node2 -> next != nullptr) {
        traverse_node2 = traverse_node2 -> next;
        count2 ++;
    }
    // if the traversing nodes are not the same after traversing the entire list
    // then the lists do not share nodes
    if (traverse_node1 != traverse_node2) {
        return -1;
    }

    Node* long_list = (count1 <= count2) ? head2 : head1;
    Node* short_list = (count1 <= count2) ? head1 : head2;

    for (int i = 0; i < std::abs(count1 - count2); i++) {
        long_list = long_list -> next;
    }

    while (short_list != long_list) {
        long_list = long_list -> next;
        short_list = short_list -> next;
    }
    return long_list -> data;
}
