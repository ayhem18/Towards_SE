# include "common.h"
# include <vector>

void inorderTraversal(Node* node, std::vector<int>& traversal) {
    if (node -> left != nullptr) {
        inorderTraversal(node -> left, traversal);
    }

    traversal.push_back(node -> data);

    if (node -> right != nullptr) {
        inorderTraversal(node -> right, traversal);
    }
}
