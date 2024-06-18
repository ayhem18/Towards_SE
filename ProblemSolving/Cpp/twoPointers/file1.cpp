# include "file1.h"

//int findFirstNode(Node* head) {
//    /**
//     * https://www.geeksforgeeks.org/problems/find-the-first-node-of-loop-in-linked-list--170645/1?page=1&category=two-pointer-algorithm&sortBy=accuracy
//     */
//
//    // let's define the first pointer
//    auto ptr1 = head;
//    auto ptr2 = head;
//
//    int n1 = 1;
//    while ((ptr1 != nullptr) && (ptr2 != nullptr)) {
//        // increment the first pointer by one node
//        ptr1 = ptr1->next;
//        n1 += 1;
//        // increment the second pointer by two nodes
//        ptr2 = ptr2->next;
//        if (ptr2 != nullptr) {
//            ptr2 = ptr2->next;
//        }
//        if (ptr1 == ptr2) {
//            break;
//        }
//    }
//
//    // there is no loop
//    if (ptr2 == nullptr) {
//        return -1;
//    }
//
//    // the length of the loop is n1 - 1
//    int loop_length = n1 - 1;
//    ptr1 = head;
//    ptr2 = head;
//    for (int i = 0; i < loop_length; i++) {
//        ptr2 = ptr2->next;
//    }
//    while (ptr1 != ptr2) {
//        ptr1 = ptr1->next;
//        ptr2 = ptr2->next;
//    }
//    return ptr1->data;
//}

# include <queue>
std::vector<long long> printFirstNegativeInteger(long long int A[],
                                                 long long int N, long long int K) {
    std::vector<long long> res = {};
    std::queue<long long> neg = {};
    for (int i = 0; i <K; i++ ) {
        if (A[i] < 0) {
            neg.push(A[i]);
        }
    }
    for (int i = 0; i <= N - K; i++) {
        if (neg.size() > 0) {
            res.push_back(neg.front());
        }
        else {
            res.push_back(0);
        }
        if (A[i] < 0) {
            neg.pop();
        }
        if (A[i + K] < 0) {
            neg.push(A[i + K]);
        }
    }
    return res;
}

