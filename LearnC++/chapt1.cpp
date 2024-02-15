/*
This file is used to illustrate some of the interesting points discussed in chpater of the C++ online tutorials that can be found here: 
https://www.learncpp.com/ 
*/

# include <iostream> 
using namespace std;

void statements() {
    // copy initialization : can get expensive with larger Data types: mainly classes 
    // (it allocates memory for the variable 'var1', then one for the value and then copy the value of the memory slot of the variable)
    double var1 = 10; 
    double var2 {10}; // list initialization : this one is preferred in general as it is faster
    std:: cout << var1 + var2 << '\n'; // it is faster to use '\n' rather than std::endl as the latter not only moves the cursor to next line but flushes the buffer... 
}


void get_input() {
    int a;
    std::cout << "please enter a number" << '\n';
    std::cin >> a;
    std::cout << "you entered " << a << "\n" << "really ? \n";
}


void naming_conventions() {
    // generally we use either camelCase or snake case for compound variable name 
    int var_name {10};
    int varName {10};
    std::cout << var_name << varName << '\n';
}

int main() {
    get_input();
}
