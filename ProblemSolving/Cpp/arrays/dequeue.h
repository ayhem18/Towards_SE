#ifndef CPP_DEQUEUE_H
#define CPP_DEQUEUE_H

# include <vector>
# include <queue>

class QueueStack{
private:
    std::queue<int> q1;
    std::queue<int> q2;
public:
    void push(int);
    int pop();
    bool empty();
};


std::vector<long long> printFirstNegativeInteger(long long int A[],
                                            long long int N, long long int K);



#endif 