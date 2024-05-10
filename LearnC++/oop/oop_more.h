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

    const double& getNumerator() const {
        return numerator;
    }

    const double& getDenominator() const {
        return denominator;
    }
// let's overload the multiplication operator using friend functions
//    friend Fraction operator * (const Fraction& f1, const double& v);
//    friend Fraction operator * (const Fraction& f1, const Fraction& f2);
//    friend Fraction operator + (const Fraction& f1, const Fraction& f2);
//    friend Fraction operator - (const Fraction& f1, const Fraction& f2);
};

// std::ostream is the type for object std::cout
std::ostream& operator<< (std::ostream& out, const Fraction& point);

Fraction operator * (const Fraction& f1, const Fraction& f2);
Fraction operator * (const Fraction& f1, const double& v);
Fraction operator + (const Fraction& f1, const Fraction& f2);
Fraction operator - (const Fraction& f1, const Fraction& f2);


#endif //LEARNC___OOP_MORE_H
