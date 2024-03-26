# include <iostream>
# include <vector>

template <typename T>
void printElement(std::vector<T>& array, int index);

// add the 'const' operator to operations where the variable is not modified
// funny enough the functions with template arguments cannot be used across files
void print_vector(const std::vector<int>& int_vec);
void print_vector(const std::vector<double>& double_vec);
std::vector<int> slice_vector(const std::vector<int>& vec,
                              int start_index,
                              int end_index);
