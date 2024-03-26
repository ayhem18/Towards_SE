//
// Created by bouab on 3/25/2024.
//

# include <iostream>
#ifndef LEARNC___BST_H
#define LEARNC___BST_H

struct Node{
    int data;
    Node * left;
    Node* right;
    Node(int val) {
        this -> data = val;
        this -> left = nullptr;
        this -> right = nullptr;
    }
};

struct NodeBST{
    int value;
    NodeBST * left;
    NodeBST * right;
    NodeBST(int val) {
        this -> value = val;
        this -> left = nullptr;
        this -> right = nullptr;
    }
};

class BST {
private:
    // the number of elements in the tree
    int size = 0;
    NodeBST *  root = nullptr;

    void m_inorder_traversal(NodeBST* head) {
        if (head == nullptr) {
            std:: cout << "The tree is empty\n";
        }
        std:: cout << head -> value;
        if (head -> left != nullptr) {
            std:: cout << " -> ";
            this -> m_inorder_traversal(head -> left);
        }

        if (head -> right != nullptr) {
            std:: cout << " -> ";
            this -> m_inorder_traversal(head -> right);
        }
    }


public:
    BST(int value) {
        // initialize the tree
        this -> root = new NodeBST(value);
    }

    // define the insertion function
    NodeBST* insert(int value) {
        NodeBST* traverse_node = this -> root;
        while (true){
            // consider the case where the value fits in the right subtree
            if (value >= (traverse_node -> value)) {
                if (traverse_node -> right == nullptr) {
                    traverse_node -> right = new NodeBST(value);
                    return traverse_node -> right;
                }
                // move to the right subtree
                traverse_node = traverse_node -> right;
            }
            // consider the case where the new value fits in the left subtree
            else {
                if (traverse_node -> left == nullptr) {
                    traverse_node -> left = new NodeBST(value);
                    return traverse_node -> left;
                }
                // move to the right subtree
                traverse_node = traverse_node -> left;
            }
        }
    }
    void inorder_traversal() {
        this ->m_inorder_traversal(this -> root);
    }
};

void freeBSTMemory(Node* head);

Node* insertNode(Node* head, int value);

bool isBST(Node* root);

int kthLargest(Node *root, int k);

Node *deleteNode(Node *root, int x);

void inorderTraversal(Node* root);

#endif //LEARNC___BST_H
