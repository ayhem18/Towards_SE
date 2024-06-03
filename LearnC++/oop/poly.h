#ifndef LEARNC___POLY_H
#define LEARNC___POLY_H

#include <string_view>

class Base
{
protected:
    int m_value {};

public:
    explicit Base(int value)
            : m_value{value} {}

    virtual std::string_view getName() const { return "Base"; };
    int getValue() const { return m_value; }

    friend std::ostream& operator << (std::ostream& out, const Base& b) {
        out << "\nBase object with value " << b.m_value;
        return out;
    }

    virtual ~Base(){};
};

class Derived: public Base
{
public:
    explicit Derived(int value)
             : Base{ value } {}

    virtual std::string_view getName() const { return "Derived"; }

    friend std::ostream& operator << (std::ostream& out, const Derived& d) {
        out << "\nDerived object with value " << d.m_value;
        return out;
    }

    int getValueDoubled() const { return m_value * 2; }
};


void polymorphism();
void function_with_inheritance();
std::string_view f(const Base& b);
#endif //LEARNC___POLY_H
