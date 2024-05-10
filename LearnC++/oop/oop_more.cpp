# include "oop_more.h"

Fraction operator * (const Fraction& f1, const Fraction& f2) {
    return {f1.getNumerator() * f2.getNumerator(),
            f1.getDenominator() * f2.getDenominator()};
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

// the code needed to overload the std::cout << operator
std::ostream& operator << (std::ostream& out, const Fraction& f) {
    out << f.getNumerator() << "/" << f.getDenominator();
    return out;
}
