# include "common.h"
# include <utility>
# include <vector>
# include <algorithm>

int getCount(Node *root, int low, int high) {
    int leftCount = 0;
    int rightCount = 0;

    if (root -> data <= low) {
        // this means that none of the nodes in the left subtree will be in the range
        if (root -> right != nullptr) {
            return (root -> data == low) + getCount(root -> right, low, high);
        }
        // if there is not left subtree return 1 if root -> data == low else 0
        return (root -> data == low);
    }

    if (root -> data > high) {
        // this means that none of the nodes in the right subtree will be in the range
        if (root -> left != nullptr) {
            return getCount(root -> left, low, high);
        }
        return 0;
    }

    // at this point we know that root -> data belongs to the [low + 1, high] range
    // and hence both left and right subtree should be considered

    if (root -> left != nullptr) {
        leftCount = getCount(root -> left, low, high);
    }

    if (root -> right != nullptr) {
        rightCount = getCount(root -> right, low, high);
    }
    return 1 + leftCount + rightCount;
}


std::pair<Node*, int> kthSmallestElementBST(Node*  root, int k, int counter) {
    int inner_counter = counter;
    if (root -> left != nullptr) {
        auto res = kthSmallestElementBST(root -> left, k, inner_counter);
        if (res.first != nullptr) {
            return res;
        }
        inner_counter = res.second;
    }

    if (inner_counter == k - 1) {
        return {root, k};
    }

    inner_counter ++;

    if (root -> right != nullptr) {
        auto res = kthSmallestElementBST(root -> right, k, inner_counter);
        if (res.first != nullptr) {
            return res;
        }
        inner_counter = res.second;
    }

    return {nullptr, inner_counter};
}
int KthSmallestElement(Node *root, int K) {
    auto res = kthSmallestElementBST(root, K, 0);
    if (res.first != nullptr) {
        return res.first -> data;
    }
    return -1;
}


int setBST(Node* root, const std::vector<int> &sortedArray, int counter) {
    int innerCounter = counter;
    if (root -> left != nullptr) {
        innerCounter = setBST(root -> left, sortedArray, innerCounter);
    }

    root -> data = sortedArray[innerCounter];
    innerCounter ++;

    if (root -> right != nullptr) {
        innerCounter = setBST(root -> right, sortedArray, innerCounter);
    }

    return innerCounter;
}
Node *binaryTreeToBST (Node *root){
    std::vector<int> values {};
    inorderTraversal(root, values);
    // sort the values
    sort(values.begin(), values.end());
    setBST(root, values, 0);
    return root;
}


int maxPathSum(Node* root) {
    int leftSum = 0, rightSum = 0;
    if (root -> left != nullptr) {
        leftSum = maxPathSum(root -> left);
    }

    if (root -> right != nullptr) {
        rightSum = maxPathSum(root -> right);
    }

    return root -> data + std::max(leftSum, rightSum);
}


std::pair<Node*, Node*> flattenBSTBothEnds(Node* root) {
    Node* newRoot = root;
    if (root -> left != nullptr) {
        auto res = flattenBSTBothEnds(root -> left);
        Node* leftSubRoot = res.first, *leftSubLeaf = res.second;
        leftSubLeaf -> right = root;
        newRoot = leftSubRoot;
    }

    // make sure to clear the left child of the root
    root -> left = nullptr;
    Node* newLeaf= root;

    if (root -> right) {
        auto res = flattenBSTBothEnds(root -> right);
        Node* rightSubRoot = res.first, *rightSubLeaf = res.second;
        root -> right =  rightSubRoot;
        newLeaf = rightSubLeaf;
    }

    return {newRoot, newLeaf};
}
Node *flattenBST(Node *root){
    auto res = flattenBSTBothEnds(root);
    return res.first;
}

void valuesInRange(Node *root, int low, int high, std::vector<int> &values) {
    if (root -> data <= low) {
        // this means that none of the nodes in the left subtree will be in the range
        if (root -> data == low) {
            values.push_back(low);
        }

        if (root -> right != nullptr) {
            valuesInRange(root -> right, low, high, values);
        }
        return;
    }

    if (root -> data > high) {
        // this means that none of the nodes in the right subtree will be in the range
        if (root -> left != nullptr) {
            valuesInRange(root -> left, low, high, values);
        }
        return;
    }

    // at this point, the function should recursively call the two subtrees
    // the left one first
    if (root -> left != nullptr) {
        valuesInRange(root -> left, low, high, values);
    }
    // the root
    values.push_back(root -> data);

    // the right subtree
    if (root -> right != nullptr) {
        valuesInRange(root -> right, low, high, values);
    }

}
std::vector<int> printNearNodes(Node *root, int low, int high) {
    std::vector<int> res{};
    valuesInRange(root, low, high, res);
    return res;
}


int addSum(Node* root, int prevSubTreeSum) {
    int rightSubTreeSum = prevSubTreeSum;
    if (root -> right != nullptr) {
        rightSubTreeSum = addSum(root -> right, prevSubTreeSum);
    }

    int leftSubTreeSum = rightSubTreeSum + root -> data;

    if (root -> right != nullptr && root -> right -> data == root -> data) {
        // this means we store the value from the right subtree, but we do not add it to the node data
        root -> data += prevSubTreeSum;
    }
    else {
        root -> data += rightSubTreeSum;
    }

    if (root -> left != nullptr) {
        return addSum(root -> left, leftSubTreeSum);
    }

    return leftSubTreeSum;
}
Node* modify(Node *root){
    addSum(root, 0);
    return root;
}
