// this file contains few remarks from the 11th chapter in the online C++ tutorials

// function overloading is such a great feat of typed functions
# include <iostream>

void functionWithNumbers(int x) {
    std::cout << "call with int " << x << "\n";
}


void functionWithNumbers(float x) {
    std::cout << "call with float " << x << "\n";
}

//void functionWithNumbers(double x) {
//    std::cout << "call with double " << x << "\n";
//}

// if we want to prevent certain types to be called with this function
//void functionWithNumbers(bool x) = delete;  // forbid calling "functionWithNumbers" with the bool argument
//void functionWithNumbers(int x) = delete;  // forbid calling "functionWithNumbers" with the bool argument

// keep in mind that deleting a function will prevent any calls that match even indirectly
//
// declaring: void f(int)  and void f(double)

// functions in C++ have default arguments that behave just like Python default args

