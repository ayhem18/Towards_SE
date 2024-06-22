#ifndef CPP_FILE2_H
#define CPP_FILE2_H

# include "common.h"

int getCount(Node *root, int l, int h);

int KthSmallestElement(Node *root, int K);

Node *binaryTreeToBST (Node *root);

int maxPathSum(Node* root);

Node *flattenBST(Node *root);

std::vector<int> printNearNodes(Node *root, int low, int high);

Node* modify(Node *root);

#endif //CPP_FILE2_H
