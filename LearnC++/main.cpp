# include <iostream>
# include <vector>

void print_vector(const std::vector<int>& int_vec);
void print_vector(const std::vector<double>& double_vec);
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

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

double max(double x, double y) {
    std::cout << "Using the 'double' version of the template 'max' function\n";
    return (x < y) ? y : x;
}

int main() {
    std:: cout << max("you", "shit")<<'\n';
    std::cout << max(1.1, 2.3)<<'\n';
    std::cout << max<double>(1.1, 2.3)<<'\n';
}
