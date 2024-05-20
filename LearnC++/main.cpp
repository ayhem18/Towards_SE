# include <algorithm>
# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "oop/oop_inheritance.h"
# include "learnCppTutorials/functions.h"
# include "CustomDS/dll.h"
# include "oop/oop_more.h"
# include "oop/more_inheritance.h"

int getInteger() {
    return 0;
}

void test_bst(){
    Node* n20 = new Node(20);
    Node* n10 = insertNode(n20, 10);
    Node* n27 = insertNode(n20, 27);
    Node* n25 = insertNode(n10, 15);
    Node* n5 = insertNode(n10, 5);
    Node* n22 = insertNode(n27, 22);

    inorderTraversal(n20);

    for (int i = 0; i < 10; i ++ ){
        int x = getInteger();
        n20 = deleteNode(n20, x);
        std::cout << "\nafter deleting " << x << '\n';
        inorderTraversal(n20);
    }
//

    freeBSTMemory(n20);
}

void play_with_fruits() {
    const Apple a{ "Red delicious", "red", 4.2 };
    const Banana b{ "Cavendish", "yellow" };
    const Fruit f {"fruit", "green"};
    std:: cout << a << "\n";
    std:: cout << b << "\n";

    std::cout << "###########################" << "\n";
    // after hiding the function some_func() in the Apple class, the line of code below does not compile
//    a.some_funct();
    b.some_funct();
}

void function_overloading() {
    functionWithNumbers(10); // int
    functionWithNumbers(10.0f); // float
//    functionWithNumbers(10.0); // double
    functionWithNumbers(true); // type expansion
    functionWithNumbers('a'); // int: type conversion
//    functionWithNumbers("Ayhem"); compilation error no match

}

void fractions_and_operators() {
    Fraction f1 {1, 2};
    Fraction f2 {2, 5}; // if b = 0, the code will raise an error
//    Fraction f3 {f1 * f2};
    Fraction f4 {f1 * 4};
//    std::cout << "f3: " << f3 <<"\n";
    std::cout << "f4: " << f4 <<"\n";
}

void dll_function() {
    DoubleLinkedList l {};
    for (int i = 1; i <= 25 ; i ++) {
        l.add(i);
    }
    int element{0};
    std::cout << "Initial list\n";
    std::cout << "list " << l << "\n";

    while (std::cin >> element) {
        std::cout << "attempting to remove " << element << "\n";
        l.remove(element);
        std::cout << "list " << l << "\n";
    }
}

void play_with_fractions_and_operators() {
    Fraction frac1;
    Fraction frac2;
    std::cout << "Enter a fraction \n";
    std::cin >> frac2;
    bool same_frac {false};

    int count = 1;
    while (!(!frac2)) {
        if (count >= 2 && frac1 == frac2){
            same_frac = true;
            break;
        }
        std::cout << "Here is the fraction you just entered: " << frac2 << "\n";
        frac1 = Fraction{frac2};
        std::cin >> frac2;
        count ++;
    }
    if (same_frac) {
        std:: cout << "You entered the same fraction twice in a row " << frac1 << "\n";
    }
    else {
        std::cout << "You entered zero " << frac2 << "\n";
    }
}


# include "small_game/game_objects.h"
# include "small_game/game_play.h"

int main()
{
//    Creature o{ "orc", 'o', 4, 2, 10 };
//    o.addGold(5);
//    o.reduceHealth(1);
//    std::cout << "The " << o.getName() << " has " << o.getHealth() << " health and is carrying " << o.getGold() << " gold.\n";
//
//    return 0;
//    Player userPlayer {getPlayerFromUser()};
//    std::cout << "Welcome " << userPlayer.getName() << "\n";
//    std::cout << "You have " << userPlayer .getHealth() << " health and are carrying " << userPlayer.getGold() << " gold.\n";

//    Monster m{ Monster::Type::orc };
//    std::cout << "A " << m.getName() << " (" << m.getSymbol() << ") was created.\n";
//    return 0;

    for (int i{ 0 }; i < 10; ++i)
    {
        Monster m{ Monster::getRandomMonster() };
        std::cout << "A " << m.getName() << " (" << m.getSymbol() << ") was created.\n";
    }
}