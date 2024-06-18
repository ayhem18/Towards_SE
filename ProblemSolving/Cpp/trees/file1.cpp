# include "file1.h"

# include <vector>
# include <queue>

std::vector<int> leftView(Node *root){
    /**
     * https://www.geeksforgeeks.org/problems/left-view-of-binary-tree/1?page=1&category=Tree&difficulty=Easy,Medium&sortBy=submissions
     */

    if (root == nullptr) {
        return {};
    }
    // create a vector for the results
    std::vector<int> res = {};
    // the queue will save both the node value and node level
    std::queue<std::pair<Node*, int>> q {};

    // push the root
    q.push({root, 1});

    int current_level = 0;

    while (! q.empty()) {
        auto p = q.front();
        Node* current_node = p.first;
        int node_level = p.second;

        if (current_level < node_level) {
            current_level = node_level;
            res.push_back(current_node -> data);
        }

        // push the left child first
        if (current_node -> left != nullptr) {
            q.push({current_node -> left, node_level + 1});
        }

        // push the right child
        if (current_node -> right != nullptr) {
            q.push({current_node -> right, node_level + 1});
        }

        q.pop();
    }
    return res;
}


/**
 *
 * "4 10 N 5 5 N 6 7 N 8 8 N 8 11 N 3 4 N 1 3 N 8 6 N 11 11 N 5 8"
 *
 * 4 10 5 6 8 11 3 5 8 8 6 11 11
 */

# include <utility>
std::vector<int> binaryTreeLeafs(Node* root) {
    if (root == nullptr){
        return {};
    }

    if (root -> right == nullptr && root -> left == nullptr) {
        return {root -> data};
    }

    std::vector<int> left_res;
    std::vector<int> right_res;

    if (root -> left != nullptr) {
        left_res = binaryTreeLeafs(root -> left);
    }

    if (root -> right != nullptr) {
        right_res = binaryTreeLeafs(root -> right);
    }

    left_res.insert(left_res.end(), right_res.begin(), right_res.end());
    return left_res;
}

std::vector<int> treeLeftMostBoundary(Node* root) {
    std::vector<int> res {};
    Node* current_node = root;
    while (current_node != nullptr) {
        res.push_back(current_node -> data);
        current_node = current_node -> left;
    }
    return res;
}

std::vector<int> treeRightMostBoundary(Node* root) {
    std::vector<int> res {};
    Node* current_node = root;
    while (current_node != nullptr) {
        res.push_back(current_node -> data);
        current_node = current_node -> right;
    }
    return res;
}

std::vector <int> boundary(Node *root) {
    std::vector<int> left = treeLeftMostBoundary(root);
    std::vector<int> right = treeRightMostBoundary(root);
    std::vector<int> leafs = binaryTreeLeafs(root);

    // the idea here is quite simple
    std::vector<int> res = {};
    res.insert(res.end(), left.begin(), left.end());

    // check if the left most element is a leaf by the way
    if (*leafs.begin() == *(left.end() - 1)) {
        res.insert(res.end(), leafs.begin() + 1, leafs.end());
    }
    else {
        res.insert(res.end(), leafs.begin(), leafs.end());
    }

    // the right most
    if (*(leafs.end() - 1) == *right.rbegin()) {
        res.insert(res.end(), right.rbegin() + 1, right.rend() - 1);
    }
    else {
        res.insert(res.end(), right.rbegin(), right.rend() - 1);
    }

    return res;
}

