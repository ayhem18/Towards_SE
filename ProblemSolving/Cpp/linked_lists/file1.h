#ifndef CPP_FILE1_H
#define CPP_FILE1_H

# include<vector>

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


#endif //CPP_FILE1_H
