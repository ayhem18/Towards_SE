#ifndef LEARNC___OOP_MORE_H
#define LEARNC___OOP_MORE_H

#include <cassert>
#include <iostream>

class Fraction {
private:
    double numerator {1};
    double denominator {1};

public:
    Fraction(double a, double b): numerator(a), denominator(b) {
        assert(b != 0 && "The denominator cannot be 0.0");
    };
    explicit Fraction(double a): Fraction(a, 1) {};

    Fraction() = default;

    const double& getNumerator() const {
        return numerator;
    }

    const double& getDenominator() const {
        return denominator;
    }

    void setNumerator(const double& val) {
        this -> numerator = val;
    }

    void setDenominator(const double& val) {
        assert (val != 0 && "The denominator cannot be set to 0");
        this -> denominator = val;
    }

// let's overload the multiplication operator using friend functions
//    friend Fraction operator * (const Fraction& f1, const double& v);
//    friend Fraction operator * (const Fraction& f1, const Fraction& f2);
//    friend Fraction operator + (const Fraction& f1, const Fraction& f2);
//    friend Fraction operator - (const Fraction& f1, const Fraction& f2);

// what about overloading the operators as member functions
    Fraction operator * (const double& v);
    // unary operators are usually implemented as member functions since they operate only on the operand:
    // the class instance
    Fraction operator - () const;
    // the '!' (logical not) operator returns 'bool'
    bool operator ! () const;

    bool operator == (const Fraction& otherFrac) const;


};

std::istream& operator >> (std::istream& in, Fraction& frac);
std::ostream& operator << (std::ostream& out, const Fraction& f);


//// std::ostream is the type for object std::cout
//// overload the output operator as a normal function
//std::ostream& operator<< (std::ostream& out, const Fraction& point);
//
//// overloaded as a normal function since the class is equipped with setters now !!
//std::istream& operator >> (std::istream& in, Fraction& frac);


//Fraction operator * (const Fraction& f1, const Fraction& f2);
//Fraction operator * (const Fraction& f1, const double& v);
Fraction operator + (const Fraction& f1, const Fraction& f2);
Fraction operator - (const Fraction& f1, const Fraction& f2);

#endif //LEARNC___OOP_MORE_H
