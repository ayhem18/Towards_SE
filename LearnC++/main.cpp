# include <algorithm>
# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "oop/oop_inheritance.h"
# include "learnCppTutorials/functions.h"
# include "CustomDS/dll.h"
# include "oop/oop_more.h"
# include "oop/more_inheritance.h"
# include "learnCppTutorials/compond_types.h"
# include "learnCppTutorials/arrays.h"

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


void fractions_and_operators() {
    Fraction f1 {1, 2};
    Fraction f2 {2, 5}; // if b = 0, the code will raise an error
//    Fraction f3 {f1 * f2};
    Fraction f4 {f1 * 4};
//    std::cout << "f3: " << f3 <<"\n";
    std::cout << "f4: " << f4 <<"\n";
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


// forward declaration to a function defined somewhere else
std::string getStringInput(const std::string& input_prompt);
//    std::cout << input_prompt <<'\n';
//    std::string input_text {};
//    std::getline(std::cin >> std::ws, input_text);
//    return input_text;
//}


# include "small_game/game_play.h"
# include "oop/poly.h"

void dll_function() {
    DoubleLinkedList<double> l {};

    for (int i = 1; i <= 3 ; i ++) {
        l.add(static_cast<double>(i));
    }
    std::cout << l.size() << "\n";

    std::cout << "Initial list\n";
    std::cout << "list " << l << "\n";

    std::vector<std::string> commands {"add", "remove", "add at", "remove at", "quit"};

    bool flag = true;
    while (flag) {
        // get the user input
        bool move = false;
        std::string user_input;
        while (! move) {
            user_input = getStringInput("Please enter the command");
            move = std::count(commands.begin(), commands.end(), user_input) != 0;
        }
        int element;
        int position;
        if (user_input == "add") {
            std::cout << "enter the element to add\n";
            std::cin >> element;
            std::cout << "attempting to add " << element << " to the list" << "\n";
            l.add(element);
        }
        else if (user_input == "add at") {
            std::cout << "enter the element and the position\n";
            std::cin >> element;
            std::cin >> position;
            std::cout << "attempting to add " << element << " to the list at position " << position << "\n";
            l.addAt(element, position);
        }

        else if (user_input == "remove") {
            std::cout << "enter the element to remove\n";
            std::cin >> element;
            std::cout << "attempting to remove " << element << "\n";
            l.remove(element);
        }

        else if (user_input == "remove at"){
            std::cout << "enter the position of the element to remove\n";
            std::cin >> position;
            std::cout << "attempting to remove the " << position << "-th element\n";
            l.removeAt(position);
        }

        else {
            flag = false;
        }
        std::cout << l << "\n";
    }

}



int main()
{
//game();
dll_function();
//array_function();
}