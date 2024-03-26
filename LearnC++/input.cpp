# include <iostream>

int getInteger() {
    int x {0};
    std:: cout << "please enter a number" << "\n";
    std::cin >> x;
    return x;
}


int getIntegerInput(const std::string& prompt_text){
    std::cout << prompt_text << '\n';
    int x {0};
    std:: cin >> x;
    return x;
}

double getOperation() {
    std::cout << "Please enter one of the following operations '+', '-', '*', '/'" << '\n';
    char op;
    std::cin >> op;
    return op;
}

