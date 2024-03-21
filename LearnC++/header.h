# include <iostream>
#ifndef LEARNC___HEADER_H
#define LEARNC___HEADER_H

struct IntPair{
    int i1{};
    int i2{};
    // non-constant member cannot be called with non-constant class objects
    void print() const{
        std::cout << "Pair (" << i1 << ", " << i2 << ")\n";
    }

    void f() {
        i1 ++;
    }
};

class C {
private:
    std::string m_name = "class";
    int m_age = 11;
public:
//    C(std::string& name, int age) {
//        this -> m_name = name;
//        this -> m_age = age;
//    }
    void print() const {
        std::cout << "My name is " << m_name << " . I am " << m_age;
    }

    void access(const C& another_c) const{
        std::cout << another_c.m_name << " is the name of the other guy";
    }

};


int function_in_global_scope() {
    std::cout << "This function is defined in the global score" << "\n";
}

namespace my_namespace {
    int add(int x, int y) {
        return x + y;
    }
    void local_function() {
        std::cout << "calling a function in the local scope" << "\n";
        function_in_global_scope();
    }
}

#endif //LEARNC___HEADER_H
