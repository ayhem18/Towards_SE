# include<array>
class Pair {
    int p1 {0};
    int p2 {0};

    bool isEqual(const Pair& anotherPair) {
        return anotherPair.p1 == p1 && anotherPair.p2 == p2;
    }
};


//class Stack {
//public:
//    int capacity {}; // this variable represents the maximum number of elements the stack can store
//    int size {0}; // this variable represents the current number of elements in the stack
//    std::array<int, capacity> _stack = {};
//
//    void push(int element) {
//
//    }
//};
