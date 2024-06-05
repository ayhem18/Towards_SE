# include "oop_more.h"

Fraction Fraction:: operator * (const double& d) const{
    return {numerator * d, denominator};
}


Fraction Fraction::operator + (const Fraction& another) const{
    double f1n = getNumerator(), f1d = getDenominator();
    double f2n = another.getNumerator(), f2d = another.getDenominator();
    return {f1n * f2d + f2n * f1d, f1d * f2d};
}

Fraction Fraction::operator + (double value) const{
     return Fraction:: operator + (Fraction{value});
}


Fraction Fraction::operator - (const Fraction& another) const{
    double f1n = getNumerator(), f1d = getDenominator();
    double f2n = another.getNumerator(), f2d = another.getDenominator();
    return {f1n * f2d - f2n * f1d, f1d * f2d};
}

Fraction Fraction::operator - (double value) const{
    return Fraction:: operator - (Fraction{value});
}

// unary operators
Fraction Fraction:: operator - () const {
    return {-getNumerator(), getDenominator()};
}

bool Fraction:: operator ! () const {
    return (getNumerator() == 0);
}

bool Fraction:: operator == (const Fraction& otherFrac) const {
    return (getNumerator() == otherFrac.getNumerator()) & (getDenominator() == otherFrac.getDenominator());
}

Fraction& Fraction::operator = (const Fraction& another) {
    // recognize self assignment
    if (*this == another) {
        return *this;
    }
    numerator = another.numerator;
    denominator = another.denominator;
    return *this;
}


// define comparison operator
bool Fraction:: operator < (const Fraction& another) const {
    return (numerator / denominator) < (another.numerator / another.denominator);
}

bool Fraction:: operator > (const Fraction& another) const {
    return (numerator / denominator) > (another.numerator / another.denominator);
}



// the code needed to overload the std::cout << operator
std::ostream& operator << (std::ostream& out, const Fraction& f) {
    out << f.getNumerator() << "/" << f.getDenominator();
    return out;
}

// the code needed to overload the std::cin >> operator;
std::istream& operator >> (std::istream& in, Fraction& frac) {
    double temp_val;
    in >> temp_val;
    frac.setNumerator(temp_val);
    in >> temp_val;
    frac.setDenominator(temp_val);
    return in;
}

// the code needed to overload the std::cout << operator
//std::ostream& operator << (std::ostream& out, const Fraction& f) {
//    out << f.getNumerator() << "/" << f.getDenominator();
//    return out;
//}
//
// the code needed to overload the std::cin >> operator;
//std::istream& operator >> (std::istream& in, Fraction& frac) {
//    double temp_val;
//    in >> temp_val;
//    frac.setNumerator(temp_val);
//    in >> temp_val;
//    frac.setDenominator(temp_val);
//    return in;
//}
