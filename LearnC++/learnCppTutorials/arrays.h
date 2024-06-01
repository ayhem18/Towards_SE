//
// Created by bouab on 6/1/2024.
//

#ifndef LEARNC___ARRAYS_H
#define LEARNC___ARRAYS_H

void array_function();

template <typename T, std::size_t N>
void pass_array_ref(std::array<T, N>& arr) {
    std::cout << "just passing an array by reference. Youha !!!\n";
}

template <typename T, std::size_t N>
void display_array(const std::array<T, N>& arr) {
    for (const T& v : arr) {
        std::cout << v << " ";
    }
    std::cout << "\n";
}



#endif //LEARNC___ARRAYS_H
