#ifndef LEARNC___HEADER_H
#define LEARNC___HEADER_H

int function_in_global_scope() {
    std::cout << "This function is defined in the global score" << "\n";
}

namespace my_namespace {
    int add(int x, int y) {
        return x + y;
    }
    void local_function() {
        std::cout << "calling a function in the local scope" << "\n";
        function_in_global_scope();
    }
}

#endif //LEARNC___HEADER_H
