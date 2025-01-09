/*
basically a file with my solutions to problems that can be solved with either a queue or a stack !!!
*/


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

/*
Solve: 
*/
# include "dequeue.h"

// there is no way to make a stack that works in O(1) for both push and pop operations

void QueueStack :: push(int x) {
    // push the element to the full queue (defaults to q1 if both are empty)
    std::queue<int>& q = (q2.empty()) ? q1 : q2; 
    q.push(x);
}   

int QueueStack :: pop() {
    std::queue<int>& qf = (q1.empty()) ? q2 : q1;
    std::queue<int>& qe =  (q1.empty()) ? q1: q2;

    while ( qf.size() > 1) {
        qe.push(qf.front());        
        qf.pop();
    }
    
    // at this point qf has only one element, the last element in the "Stack"
    int lastVal = qf.front();
    qf.pop();
    return lastVal;
}


bool QueueStack :: empty() {
    return (q1.empty()) && (q2.empty());
}

