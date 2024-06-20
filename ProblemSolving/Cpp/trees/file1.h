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

std::vector<int> topView(Node *root);

std::pair<int, int> depth_and_diameter(Node* root);

bool isSumTree(Node* root);

std::vector<int> verticalOrder(Node *root);

Node* lca(Node* root ,int n1 ,int n2 );

std::pair<Node*, std::pair<int, int>> lca_distance(Node* root, int n1, int n2);

int findDist(Node* root, int a, int b);

#endif //CPP_FILE1_H
