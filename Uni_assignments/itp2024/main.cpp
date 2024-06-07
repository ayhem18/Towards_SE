# include <iostream>
# include <vector>
# include "labs/objects.h"

void lab2_task1_main() {
    // conversion constructor
    Box b1 {1};
    std::cout << "b1 : " << b1 << "\n";
    // copy constructor
    Box b2 {b1};
    std::cout << "b2 : " << b2 << "\n";

    Box b3 {2, 4, 5};
    std::cout << "b3: " << b3 << "\n";
    b3 = b2;
    std::cout << "b3 again " << b3 << "\n";
    b3 = b3 * 4;
    std::cout << "b3 after scaling " << b3 << "\n";
}

void lab3_task_main () {
    // this function mainly considers polymorphism

    // create a vector of Animals
    std::vector<Animal*> animals {new Dolphin("d1", 10),
                                  new Lion("l1", 5),
                                  new Lion("l2", 15),
                                  new Lion("l3", 9),
                                  new Dolphin("d2", 2)
                                  };

    // iterate and call the sounds
    for (Animal* ap : animals) {
        std:: cout << ap -> make_sound() << "\n";
    }

    for (auto & a: animals) {
        std:: cout << *a;
    }

    for (auto & animal : animals) {
        free(animal);
    }
}

void lab4_task1_main() {
    SavingAccount s1 {1, 1000, "ayhem", 0.05};

    // the line below would not compile since the copy constructor is deleted in the 'Account' class
//    SavingAccount s2 {s1};
    // the line below would not compile since the = operator is deleted in the 'Account' class
    SavingAccount anotherAcc {2, 500, "another", 0.025};
    //
//    anotherAcc = s1;
}

//int main() {
//}
