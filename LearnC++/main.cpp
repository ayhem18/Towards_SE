# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "learnCppTutorials/functions.h"
# include "oop/more_inheritance.h"
# include "oop/oop_more.h"

void oop_custom_containers();
void arrayListFunction();
void dll_function();
void test_bst();

// let's play with class template
template <typename T = std::string>
class cls{
public:
    cls() = default;
    bool lessThan (const T& v1, const T& v2) {
        std::cout << "\ncalling the general member function\n";
        return v1 < v2;
    }
};

template <>
class cls<double>{
public:
    cls() = default;
    bool lessThan (const double& v1, const double& v2) {
        std::cout << "\ncalling the special double member function\n";
        return abs(v1) < abs(v2);
    }
};


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


template<typename T>
class Auto_ptr3
{
    T* m_ptr {};
public:
    Auto_ptr3(T* ptr = nullptr)
            : m_ptr { ptr }
    {
    }

    ~Auto_ptr3()
    {
        delete m_ptr;
    }

    // Copy constructor
    // Do deep copy of a.m_ptr to m_ptr
    Auto_ptr3(const Auto_ptr3& a)
    {
        m_ptr = new T;
        *m_ptr = *a.m_ptr;
    }

    // Copy assignment
    // Do deep copy of a.m_ptr to m_ptr
    Auto_ptr3& operator=(const Auto_ptr3& a)
    {
        // Self-assignment detection
        if (&a == this)
            return *this;

        // Release any resource we're holding
        delete m_ptr;

        // Copy the resource
        m_ptr = new T;
        *m_ptr = *a.m_ptr;

        return *this;
    }

    T& operator*() const { return *m_ptr; }
    T* operator->() const { return m_ptr; }
    bool isNull() const { return m_ptr == nullptr; }
};

class Resource
{
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
};

Auto_ptr3<Resource> generateResource()
{
    Auto_ptr3<Resource> res{new Resource};
    return res; // this return value will invoke the copy constructor
}

//int main()
//{
//    Auto_ptr3<Resource> mainres;
//    mainres = generateResource(); // this assignment will invoke the copy assignment
//
//    return 0;
//}


int main() {
//game();
//dll_function();
//array_function();
//arrayListFunction();
//oop_custom_containers();

    Auto_ptr3<Resource> mainres;
    mainres = generateResource(); // this assignment will invoke the copy assignment
    return 0;

}