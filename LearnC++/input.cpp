# include <iostream>

int getInteger() {
    int x {0};
    std::cin >> x;
    return x;
}


double getNumber() {
    std::cout << "Please enter a number" << '\n';
    double x {0};
    std:: cin >> x;
    return x;
}

double getOperation() {
    std::cout << "Please enter one of the following operations '+', '-', '*', '/'" << '\n';
    char op;
    std::cin >> op;
    return op;
}

