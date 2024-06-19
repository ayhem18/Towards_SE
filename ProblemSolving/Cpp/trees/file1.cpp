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
    /**
     * the solution below keeps raising an error on the GFG server...
     * well I am kinda proud of the solution, but have no clue how to fix the error (19th of June 2024)
     */

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

# include<algorithm>

std::vector<int> topView(Node *root) {
    std::queue<std::pair<Node*, std::pair<int, int>>> q;
    q.push({root, { 0, 0}});
    std::vector<std::vector<int>> res;

    while (! q.empty()) {
        auto current_node  = q.front();
        Node* node = current_node.first;
        int level = current_node.second.first, pos = current_node.second.second;

        if (node -> left != nullptr) {
            q.push({node -> left, {level + 1, pos - 1}});
        }

        if (node -> right != nullptr) {
            q.push({node -> right, {level + 1, pos + 1}});
        }
        // add it to the vector
        res.push_back({node -> data, level, pos});
        // remove it from the queue
        q.pop();
    }

    auto comparison_function = [] (std::vector<int>& v1, std::vector<int>& v2) -> bool {
        int level1 = v1[1];
        int level2 = v2[1];
        int pos1 = v1[2], pos2 = v2[2];

        if (pos1 < pos2) {
            return true;
        }

        if (pos1 > pos2) {
            return false;
        }

        return level1 < level2;
    };

    // time to sort the vector
    std::sort(res.begin(), res.end(), comparison_function);
    int current_pos = res[0][2];
    std::vector<int> final_res {res[0][0]};

    for (auto& v: res) {
        int pos = v[2];
        if (pos > current_pos) {
            current_pos = pos;
            final_res.push_back(v[0]);
        }
    }
    return final_res;
}


std::pair<int, int> depth_and_diameter(Node* root) {
    int leftDepth = 0, rightDepth = 0;
    int leftDiameter = 0, rightDiameter = 0;

    if (root -> left != nullptr) {
        auto leftPair = depth_and_diameter(root -> left);
        leftDepth = leftPair.first;
        leftDiameter = leftPair.second;
    }

    if (root -> right != nullptr) {
        auto rightPair = depth_and_diameter(root -> right);
        rightDepth = rightPair.first;
        rightDiameter = rightPair.second;
    }

    // as for the depth
    int depth = 1 + std::max(leftDepth, rightDepth);

    int diameter = std::max(leftDiameter, rightDiameter);
    diameter = std::max(1 + leftDepth + rightDepth, diameter);

    return {depth, diameter};
}

int diameter(Node* root) {
    auto res = depth_and_diameter(root);
    return res.second;
}

