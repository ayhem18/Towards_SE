// lvalue: is an expression that evaluates to an object (with an address in memory)
// rvalue: basically a literal; an object with no address in memory

#include<iostream>

void func() {
    int var {1};
    int& ref_var {var};
    // modify ref_var <=> modify var
    const int cnst_var{1};
    const int & cnt_ref {cnst_var};

    // question why would I care about const reference:
    // they extend the lifetime of the temporary object assigned to it
     // int& var {5}; does not compile; because it '5' is an rvalue
     const int & cnt_ref_var {5}; // now cnt_ref_var is just another constant variable holding the value 5

     // a little bit more about pointers

}


void pointers_stuff() {
    // make sure to set any pointer to nullptr after using it
    int var{5};
    int* pt = &var;
    std::cout << "deferring the pointer to var " << *pt <<"\n";
    *pt += 1;
    std::cout << "checking the variable var " << var <<"\n";

    int* const cnt_pt = &var; // the pointer itself is cnst: cannot change the address it points to !!
    *cnt_pt += 1; // can modify the value of the variable the pointer is pointing to

    //
    // make sure to free the memory
    free(pt);
    free(cnt_pt);
}


void printByAddress(const int* ptr)
{
    // the value pointed by the pointer is constant, not the pointer itself
    std::cout << *ptr << '\n';
    // *ptr += 1; // this is  allowed if we remove the const keyword
}

void passByAddressCopy(int* ptr) {
    // the point here is that 'ptr' represents a copy of the actual pointer
    // we can modify the data by dereferring ptr, but cannot change the actual pointer...

}