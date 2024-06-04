# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "learnCppTutorials/functions.h"
# include "oop/more_inheritance.h"
# include "oop/oop_more.h"

void oop_custom_containers();
void arrayListFunction();
void dll_function();
void test_bst();

// let's play with class template
template <typename T>
class cls{
public:
    cls() = default;
    bool lessThan (const T& v1, const T& v2) {
        std::cout << "\ncalling the general member function\n";
        return v1 < v2;
    }
};

template <>
class cls<double>{
public:
    cls() = default;
    bool lessThan (const double& v1, const double& v2) {
        std::cout << "\ncalling the special double member function\n";
        return abs(v1) < abs(v2);
    }
};


int main() {
//game();
//dll_function();
//array_function();
//arrayListFunction();
//oop_custom_containers();

cls<double> c1 {};
std::cout << c1.lessThan(-4, 2) <<"\n";
cls<int> c2 {};
std::cout << c2.lessThan(-4, 2) <<"\n";
}