// lvalue: is an expression that evaluates to an object (with an address in memory)
// rvalue: basically a literal; an object with no address in memory

# include<iostream>
# include "strings.h"
# include <algorithm>

void func() {
    int var {1};
    int& ref_var {var};
    // modify ref_var <=> modify var
    const int cnst_var{1};
    // keep the const modifier here !!! a modifiable lvalue ref cannot be bound to
    // a non-modifiable lvalue ref
    const int & cnt_ref {cnst_var};

    // question why would I care about const reference:
    // they extend the lifetime of the temporary object assigned to it
     // int& var {5}; does not compile; because it '5' is an rvalue
     const int & cnt_ref_var {5}; // now cnt_ref_var is just another constant variable holding the value 5
     // a little bit more about pointers
}

void reference_stuff() {
    int var {1};
    int& ref_var{var};
    // ref_var is a copy of 'var' basically
    std::cout << ref_var << "\n";
    var ++;
    std::cout << ref_var << "\n";

    int v {2};
    const int& r{v}; // basically means that the variable 'v' cannot be changed through the reference
    // useful in functions

    v ++;
    std:: cout << r << "\n";
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

}


void printByAddress(const int* ptr)
{
    // the value pointed by the pointer is constant, not the pointer itself
    std::cout << *ptr << '\n';
    // *ptr += 1; // this is  allowed if we remove the const keyword
}

void passByAddressCopy(int* ptr) {
    // the point here is that 'ptr' represents a copy of the actual pointer
    // we can modify the data by de-referring ptr, but cannot change the actual pointer...
}


void dynamic_array_allocation() {
    // first ask the user for the number of names
    std::cout << "How many names would like to enter\n";
    int num_names;
    std::cin >>num_names;

    // allocated a dynamic array
    std::string* names = new std::string[num_names];

    for (int i = 0; i < num_names; i ++ ) {
        std::string p = "Please enter the name number "  + std::to_string(i + 1);
        std::string name {getStringInput(p)};
        names[i] = name;
    }

    // sort the names
    std::sort(names, names + num_names);

    std::cout << "Here is the sorted the list of names\n";
    for (int i = 0; i < num_names; i ++) {
        std::cout << "name number " << i << " " << names[i] << "\n";
    }

    // free the memory
    delete [] names;
}



void references_move() {
    int x {10};
    int& ref1 {x};
    const int& ref2 {10};

}