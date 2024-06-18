#ifndef CPP_FILE1_H
#define CPP_FILE1_H

# include <vector>

struct Node{
    int data;
    struct Node* left;
    struct Node* right;

    Node(int x){
        data = x;
        left = right = nullptr;
    }
};


std::vector<int> leftView(Node *root);

std::vector <int> boundary(Node *root);

#endif //CPP_FILE1_H
