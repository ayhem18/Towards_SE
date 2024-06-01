// this script was created to learn more about arrays in c++

# include <array>
# include <iostream>
# include "arrays.h"
//template <typename T>
//void display_array(const std::array<T> & array) {
//
//}


void array_function() {
//    std::array<double, 10> array {};
//    array[0] = 5.4;
//

//    std::array<int, 365> temps {1};
//    std::cout << temps[10] << "\n";

    std::array word {'h', 'e', 'l', 'l', 'o'};
    std::cout << word[1] << "\n";
    display_array(word);
    //
//    const std::array array {1.2, 2.1, 3.7};
//
//    for (double v: array) {
//        std::cout << v << " ";
//    }
//    std::cout << "\n";
//
//    for (double v : array) {
//        v++;
//    }
//
//    std::cout << "after loop \n";
//
//    for (double v: array) {
//        std::cout << v << " ";
//    }
//    std::cout << "\n";

}

