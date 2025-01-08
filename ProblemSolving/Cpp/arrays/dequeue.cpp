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
