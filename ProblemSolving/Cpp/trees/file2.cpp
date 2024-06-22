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
