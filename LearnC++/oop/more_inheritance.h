# include <iostream>

class Base
{
public:
    Base()
    {
        std::cout << "Base()\n";
    }

    // every derived class constructor calls at least one base class constructor
    // if no derived class constructor is specified, the default one will be called
    // (whether created explicitly or using the default one)
    // deleting the default one without creating an explicit constructor will prevent inheritance
     ~Base()
    {
        std::cout << "~Base()\n";
    }
};

class Derived: public Base
{
public:
    Derived()
    {
        std::cout << "Derived()\n";
    }
    ~Derived()
    {
        std::cout << "~Derived()\n";
    }
};

