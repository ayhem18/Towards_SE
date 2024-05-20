# include "oop_more.h"

Fraction Fraction:: operator * (const double& d) {
    return {numerator * d, denominator};
}

Fraction operator * (const Fraction& f1, const double& v){
    return {f1.getNumerator() * v,f1.getDenominator()};
}


Fraction operator + (const Fraction& f1, const Fraction& f2) {
    double f1n = f1.getNumerator(), f1d = f1.getDenominator();
    double f2n = f2.getNumerator(), f2d = f2.getDenominator();
    return {f1n * f2d + f2n * f1d, f1d * f2d};
}

Fraction operator - (const Fraction& f1, const Fraction& f2) {
    double f1n = f1.getNumerator(), f1d = f1.getDenominator();
    double f2n = f2.getNumerator(), f2d = f2.getDenominator();
    return {f1n * f2d - f2n * f1d, f1d * f2d};
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
