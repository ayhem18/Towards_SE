# include <iostream>
# include <vector>
# include "containers.h"

template <typename T>
void printElement(std::vector<T>& array, int index) {
    if (index < 0 | index >= array.size()) {
        std::cout << "You cannot access element with index "
                  << index
                  << " from an array with length "
                  << array.size()
                  << '\n';
        return;
    }
    std::cout << "The element at index "  << index << " is " << array[index] << '\n';
}


// add the 'const' operator to operations where the variable is not modified
// funny enough the functions with template arguments cannot be used across files
void print_vector(const std::vector<int>& int_vec) {
    for (int element: int_vec) {
        std::cout << element << ' ';
    }
    std::cout << '\n';
}

void print_vector(const std::vector<double>& double_vec){
    for (double element: double_vec) {
        std:: cout << element << ' ';
    }
    std::cout << '\n';
}

std::vector<int> slice_vector(const std::vector<int>& vec,
                              int start_index,
                              int end_index) {
    auto first = vec.begin() + start_index;
    auto last  = vec.begin() + end_index + 1;
    return std::vector(first, last);
}



template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

double max(double x, double y) {
    std::cout << "Using the 'double' version of the template 'max' function\n";
    return (x < y) ? y : x;
}
