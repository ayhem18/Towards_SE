#ifndef CPP_COMMON_H
#define CPP_COMMON_H

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

void inorderTraversal(Node* node, std::vector<int>& traversal);


#endif //CPP_COMMON_H
