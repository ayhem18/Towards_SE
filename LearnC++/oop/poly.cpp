// this script illustrates some important ideas on C++ polymorphism
# include <iostream>
# include "poly.h"

// the piece of code commented below will always run the base function although the actual type
// is Derived and not Base


void function_with_inheritance() {
Derived d{1};
Base* pB {&d};
std::cout << pB -> getName() << "\n";
Base& rB {d};
std::cout << rB.getName() << "\n";
Base cB{d};
std::cout << cB.getName() << "\n";
}

void polymorphism() {
    Derived d{10};
    Base* pD = &d;
    std::cout << pD -> getName() << "\n"; // this will print the derived class version

    // let's check with a reference
    Base& rD {d};
    std::cout << rD.getName() << "\n";

    Base derived_copy {d};
    std::cout << derived_copy.getName() << "\n"; // this will always print the original class version

}

