/*
This file is used to illustrate some of the interesting points discussed in chapter 2 of the C++ online tutorials that can be found here: 
https://www.learncpp.com/ 
*/

# include <iostream> 
using namespace std;

// functions

int value_return_function() {
    int a = 10;
    std:: cout << a << '\n';
    // not returning the value will raise warning but not necessarily a compilation error.
    return a;
}

// unlike Python, C++ functions can return one and only value (it it is not a void function that is)
// unlike Python, C++ does not allow nested functions.


int function(int a, int b) {
    // a, b are function parameters
    // the values passed by the user to the function are called arguments
    
    // this is pass by value. When the function is called, then some variables (with the name a and b) are created, and the arguments then copied into
    // these variables, this might get pretty slow with certain objects. 

    // keep in mind that with pass by value, the variable passed as an argument will not be modified 
    // as its value is copied to another variable created in the scope of the function

    return a + b;
}

// this function won't compile 

// void foo() {
//     // return 1;
// }


// this will lead to undefined behavior
// int foo() {
// }


/*
Let's talk scopes...
so scope is basically the part of the code where a certain variable can be seen and used. IT is is a compile-time property.

a local variable can only be seen and used with in body function where it is defined.
*/





