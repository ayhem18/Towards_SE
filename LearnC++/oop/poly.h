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
    virtual int abstract_function() const = 0;
    virtual ~Base(){};
};

class Derived: public Base
{
public:
    explicit Derived(int value)
             : Base{ value } {}

    virtual std::string_view getName() const { return "Derived"; }

    int abstract_function() const {
        return 0;
    }

    int getValueDoubled() const { return m_value * 2; }
};


void polymorphism();
void function_with_inheritance();

#endif //LEARNC___POLY_H
