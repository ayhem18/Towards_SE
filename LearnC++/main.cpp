# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "learnCppTutorials/functions.h"
# include "oop/more_inheritance.h"
# include "oop/oop_more.h"
# include <array>
# include "string.h"

void oop_custom_containers();
void arrayListFunction();
void dll_function();
void test_bst();

//// let's play with class template
//template <typename T = std::string>
//class cls{
//public:
//    cls() = default;
//    bool lessThan (const T& v1, const T& v2) {
//        std::cout << "\ncalling the general member function\n";
//        return v1 < v2;
//    }
//};
//
//template <>
//class cls<double>{
//public:
//    cls() = default;
//    bool lessThan (const double& v1, const double& v2) {
//        std::cout << "\ncalling the special double member function\n";
//        return abs(v1) < abs(v2);
//    }
//};


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


int fac(int N) {
    if (N == 0) {
        return 1;
    }
    return N * fac(N - 1);
}

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

void function();


template <typename T>
concept greaterThan = requires(T a, T b) { a > b;};

template <typename T>
concept lessThan = requires(T a, T b) { a < b;};

//template <typename T>
//concept IntAddable = requires (T a, int b) {a + b;};

// let's code the barrier function from the itp2 lecture
template <typename T>
void alignArray( T* array, int size, T barrier ) requires greaterThan<T> && lessThan<T>
{
    for ( int i=0; i < size; i++ )
    {
        if ( array[i] < barrier )
            array[i] = array[i] + 2.0;
        else if ( array[i] > barrier )
            array[i] = array[i] - 2.0;
    }
}

template <typename T>
requires lessThan<T>
class cls {
private:
    T m_value;
public:
    explicit cls(const T& value): m_value(value){}

    bool operator < (const cls another) {
        return m_value < another.m_value;
    }
};

template <>
class cls <char*> {
private:
    char* m_value;
public:
    cls(char* value): m_value(value){}
    bool operator < (const cls another) {
        return strcmp(m_value, another.m_value) < 0;
    }
};


int main() {
//game();
//dll_function();
//array_function();
//arrayListFunction();
//oop_custom_containers();



Fraction a[] = {Fraction(3, 4)
                , Fraction(1, 2),
                Fraction(-3, 7),
                Fraction {15,4}};

//// let's call the alignArray with the Fraction class
Fraction barrier {1, 2};
alignArray(a, 4, barrier);
//
std::cout << a[0] << " " << a[1] << " " << a[2] << " " << a[3] << " "  << "\n";
}