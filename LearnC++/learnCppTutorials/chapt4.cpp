/*
This file contains some notes from the 4th chapter of the C++ online tutorials: https://www.learncpp.com/ 
*/
#include <iostream>

void bool_data_type() {
    bool btrue {1};
    bool bfalse {0};
    std::cout << "true bool as : " << btrue << std::endl;
    std::cout << "false bool as : " << bfalse << std::endl;

    std::cout << std::boolalpha; // I'd like to think of it as if I am passing some code to teh output stream to display 'true' as True and not 1

    std::cout << "true bool as : " << btrue << std::endl;
    std::cout << "false bool as : " << bfalse << std::endl;
}
