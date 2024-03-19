// lvalue: is an expression that evaluates to an object (with an address in memory)
// rvalue: basically a literal an object with no address in memory
#include<iostream>


// this part contains code about references
void function_const_int_ref(const int & x) {
    std::cout << x <<'\n';
}

void function_int_ref(int& x) {
    std::cout << "before " << x << '\n';
    x++;
    std::cout << "after " << x << '\n';
}

void function() {
    int x = {10};
    const int &ref{x};
    std::cout << x << ref << '\n'; //1010
    x++;
    std::cout << x << ref << '\n';  // 1111
}

// this part contains code about pointers

void pointers() {
    int x {10};
    int* x_ptr {&x}; // x_ptr is a variable whose value is the address of the variable 'x' in memory
    // we can use the pointer to actually set the value of x
    std::cout << std::boolalpha << ((*x_ptr) == x);
    std::cout << x << '\n';
}