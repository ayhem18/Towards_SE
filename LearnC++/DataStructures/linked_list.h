#ifndef LEARNC___LINKED_LIST_H
#define LEARNC___LINKED_LIST_H

struct Node {
    int data;
    struct Node *next;
    Node(int val)
    {
        data=val;
        next= nullptr;
    }
};


// function to insert a node to a linked list
Node* insert_element(Node * head, int value);
// function to print the elements of a linked list
void print_linked_list(Node* head);

// a function to determine whether a linked list has a cycle or not
bool hasCycle(Node *head);

int countNodesinLoop(struct Node *head);

Node* findIntersection(Node* head1, Node* head2);

#endif //LEARNC___LINKED_LIST_H
