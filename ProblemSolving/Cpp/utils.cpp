# include <cassert>
int mod(int a, int b) {
    // returns a positive value of the expression (a mod b)
    return ((a % b) + b) % b;
}

long long int mod(long long int a, long long int b) {
    // returns a positive value of the expression (a mod b)
    return ((a % b) + b) % b;
}
