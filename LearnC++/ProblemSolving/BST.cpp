#include "BST.h"


//struct Node{
//    int data;
//    Node * left;
//    Node* right;
//    Node(int val) {
//        this -> data = val;
//        this -> left = nullptr;
//        this -> right = nullptr;
//    }
//};

#include <limits>
//your code here
int max_int = std::numeric_limits<int>::max();
int min_int = std::numeric_limits<int>::min();


void inorderTraversal(Node* head) {
    if (head == nullptr) {
        std:: cout << "The tree is empty\n";
        return;
    }

    if (head -> left != nullptr) {
        inorderTraversal(head -> left);
    }

    std:: cout << head -> data;
    std:: cout << " -> ";

    if (head -> right != nullptr) {
        inorderTraversal(head -> right);
    }
}

bool isBSTMinMax(Node* root, int minValue, int maxValue) {
    if ((minValue > root -> data) || (root -> data > maxValue)) {
        return false;
    }

    bool left;
    bool right;
    if (root -> left == nullptr) {
        left = true;
    }
    else {
        left = isBSTMinMax(root -> left, minValue, root -> data);
    }
    if (! left) {
        return false;
    }

    if (root -> right == nullptr) {
        right = true;
    }
    else {
        right = isBSTMinMax(root -> right, root -> data, maxValue);
    }
    if (! right) {
        return false;
    }
    return right;
}

bool isBST(Node* root) {
    return isBSTMinMax(root, min_int, max_int);
}

// insert a new node to a given BST
Node* insertNode(Node* root, int value) {
    Node* traverse_node = root;
    while (true){
        // consider the case where the value fits in the right subtree
        if (value >= (traverse_node -> data)) {
            if (traverse_node -> right == nullptr) {
                traverse_node -> right = new Node(value);
                return traverse_node -> right;
            }
            // move to the right subtree
            traverse_node = traverse_node -> right;
        }
            // consider the case where the new value fits in the left subtree
        else {
            if (traverse_node -> left == nullptr) {
                traverse_node -> left = new Node(value);
                return traverse_node -> left;
            }
            // move to the right subtree
            traverse_node = traverse_node -> left;
        }
    }
}

// find the minimum value in a BST
int smallestValue(Node* root) {
    Node* traverse_node = root;
    while (traverse_node -> left != nullptr) {
        traverse_node = traverse_node -> left;
    }
    return traverse_node -> data;
}


// this function finds the lowest common ancestor of 2 values in a binary search tree
Node* LCA(Node *root, int n1, int n2) {
    int min = std::min(n1, n2);
    int max = std::max(n1, n2);

    // this means that n1 and n2 are in different subtrees
    if ((root -> data < max) && (root -> data > min)) {
        return root;
    }

    // first let's consider some base cases
    if ((root -> data == n1) || (root -> data == n2)) {
        return root;
    }

    // if the value at the root is larger than both values,
    // then n1 & n2 lie in the left subtree
    if (root -> data > max) {
        return LCA(root -> left, n1, n2);
    }

    if (root -> data < min) {
        return LCA(root -> right, n1, n2);
    }
}

// in order to solve the find the k-th largest element in a given BST
// we need 2 others auxiliary functions: one that counts the number of elements in a given bst
// and one that finds the largest elements in a given bst
int largestValue(Node* root) {
    Node* traverse_node = root;
    while (traverse_node -> right != nullptr) {
        traverse_node = traverse_node -> right;
    }
    return traverse_node -> data;
}
// this function counts the number of elements in a given binary search tree
int bstCount(Node* root) {
    int left_count = 0;
    int right_count = 0;
    if (root -> right != nullptr) {
        right_count = bstCount(root -> right);
    }

    if (root -> left != nullptr) {
        left_count = bstCount(root -> left);
    }
    return 1 + left_count + right_count;
}
// this function finds the k-th largest element in a binary search tree
int kthLargest(Node *root, int k)
{
    // let's start with the base case:
    if (k == 1) {
        return largestValue(root);
    }

    // at this point we know that k is larger than 1
    if (root -> right == nullptr) {
        return kthLargest(root -> left, k - 1);
    }

    // count the number of elements to the right
    int right_count = bstCount(root -> right);

    // there are 3 cases here
    if (right_count == k - 1) {
         return root -> data;
    }

    if (right_count >= k ) {
        // this means the k-th largest element is in the right subtree
        return kthLargest(root -> right, k);
    }

    // this means that we have right_count < k - 1
    return kthLargest(root -> left, k - right_count - 1);
}

// time to delete some nodes from a given bst
Node *deleteNode(Node *root, int x) {
    // let's start with the case where root contains the value 'X'

    // case
    if (root -> data == x){
        // find either the smallest value in the right subtree
        // or the largest one in the left subtree
        int next_value;
        if (root -> right != nullptr) {
            next_value = smallestValue(root -> right);
        }
        else {
            // we are discarding the degenerate case where there is only one element in the tree
            next_value = largestValue(root -> left);
        }
        // create a new root
        Node* new_root =  new Node(next_value);

        new_root -> left = root -> left;
        new_root -> right = root -> right;
        free(root);

        return new_root;
    }

    // at this point we know that the root does not contain the value we are looking for
    Node* traverse_node = root;
    while (traverse_node != nullptr) {
        if (traverse_node -> data < x) {
            // we know that the 'X' is on the right subtree
            if (traverse_node -> right == nullptr) {
                // we know that 'X' is on the right subtree but there is no right subtree
                // nothing to delete -> return
                return root;
            }
            if (traverse_node -> right -> data == x) {
                // remove the root of the subtree
                // if 'x' has no children
                if ((traverse_node -> right -> right == nullptr) && (traverse_node -> right -> left == nullptr)) {
                    free(traverse_node->right);
                    traverse_node->right = nullptr;
                    return root;
                }

                int nextValue;
                if (traverse_node -> right -> right != nullptr) {
                    nextValue = smallestValue(traverse_node -> right -> right);
                }
                else {
                    nextValue = largestValue(traverse_node -> right -> left);
                }

                Node* new_node =  new Node(nextValue);
                new_node -> left = traverse_node -> right -> left;
                new_node -> right = traverse_node -> right -> right;
                free(traverse_node -> right);
                // make sure to link
                traverse_node -> right = new_node;
                return root;
            }
        }

        // 'X' is on the left subtree
        else {
            // we know that the 'X' is on the left subtree
            if (traverse_node -> left == nullptr) {
                // we know that 'X' is on the left subtree but there is right subtree
                // nothing to delete -> return
                return root;
            }
            if (traverse_node -> left -> data == x) {
                // remove the root of the subtree
                // if 'x' has no children
                if ((traverse_node -> left -> right == nullptr) && (traverse_node -> left -> left == nullptr)) {
                    free(traverse_node->left);
                    traverse_node->left = nullptr;
                    return root;
                }

                int nextValue;
                if (traverse_node -> left -> right != nullptr) {
                    nextValue = smallestValue(traverse_node -> left -> right);
                }
                else {
                    nextValue = largestValue(traverse_node -> left -> left);
                }

                Node* new_node =  new Node(nextValue);
                new_node -> left = traverse_node -> left -> left;
                new_node -> right = traverse_node -> left -> right;
                free(traverse_node -> right);
                // make sure to link
                traverse_node -> left = new_node;
                return root;
            }
        }
    }
}


void freeBSTMemory(Node* head){
    if (head -> left != nullptr) {
        freeBSTMemory(head -> left);
    }
    if (head -> right != nullptr) {
        freeBSTMemory(head -> right);
    }
    free(head);
}


