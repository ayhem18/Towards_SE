#ifndef CPP_FILE1_H
#define CPP_FILE1_H


// define the Node used for Linked Lists
struct Node {
    int data;
    struct Node *next;

    Node(int x) {
        data = x;
        next = nullptr;
    }
};

int findFirstNode(Node* head);

int countDistinctSubarray(int arr[], int n);

#endif //CPP_FILE1_H
