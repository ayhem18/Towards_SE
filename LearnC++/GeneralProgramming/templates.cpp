# include <iostream>
# include "string.h"

template <typename T>
T max(T x, T y) {
    std::cout << "calling the general max function\n";
    return (x <= y) ? y : x;
}

// explicit specialization of the template function
// will be called both for max(bool args) and max<bool>(args)
template <>
bool max<bool>(bool b1, bool b2) {
    std::cout << "calling the bool function\n";
    return (b1 <= b2) ? b2 : b1;
}

// usual function will only be called when the '<>' is omitted.
bool max(bool b1, bool b2) {
    std::cout << "calling the bool function\n";
    return (b1 <= b2) ? b2 : b1;
}

// template function overloading
template <typename T>
T max(T* ptrX, T* ptrY) {
    return max(*ptrX, *ptrY);
}

// non-type template
template <int N>
int factorial() {
    static_assert(N >= 0, "factorial: N must be non-negative");
    return N * factorial<N - 1>();
}
template <>
int factorial<1>() {
    return 1;
}

template <>
int factorial<0>() {
    return 1;
}


// // concepts and class specializations !!!
// template <typename T>
// concept greaterThan = requires(T a, T b) { a > b;};

// template <typename T>
// concept lessThan = requires(T a, T b) { a < b;};


// template <typename T>
// requires lessThan<T>
// class cls {
// private:
//     T m_value;
// public:
//     explicit cls(const T& value): m_value(value){}

//     bool operator < (const cls another) {
//         return m_value < another.m_value;
//     }
// };

// template <>
// class cls <char*> {
// private:
//     char* m_value;
// public:
//     cls(char* value): m_value(value){}
//     bool operator < (const cls another) {
//         return strcmp(m_value, another.m_value) < 0;
//     }
// };


// // let's code the barrier function from the itp2 lecture
// template <typename T>
// void alignArray( T* array, int size, T barrier ) requires greaterThan<T> && lessThan<T>
// {
//     for ( int i=0; i < size; i++ )
//     {
//         if ( array[i] < barrier )
//             array[i] = array[i] + 2.0;
//         else if ( array[i] > barrier )
//             array[i] = array[i] - 2.0;
//     }
// }