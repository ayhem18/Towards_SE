# include <iostream>
# include <vector>

// add the 'const' operator to operations where the variable is not modified
// funny enough the functions with template arguments cannot be used across files
void print_vector(std::vector<int>& int_vec) {
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