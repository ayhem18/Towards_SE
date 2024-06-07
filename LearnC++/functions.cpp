# include <algorithm>
# include "containers.h"
# include "ProblemSolving/BST.h"
# include "oop/oop_starter.h"
# include "oop/oop_inheritance.h"
# include "learnCppTutorials/functions.h"
# include "CustomDS/data_structures/DLL.h"
# include "oop/oop_more.h"
# include "oop/more_inheritance.h"
# include "learnCppTutorials/strings.h"
# include "CustomDS/data_structures/ArrayList.h"
# include "small_game/game_play.h"

int mod(int value, int mod) {
    return ((value % mod) + mod) %  mod;
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
    Fraction f4 {f1 * 4.0};
//    std::cout << "f3: " << f3 <<"\n";
    std::cout << "f4: " << f4 <<"\n";
}

//void play_with_fractions_and_operators() {
//    Fraction frac1;
//    Fraction frac2;
//    std::cout << "Enter a fraction \n";
//    std::cin >> frac2;
//    bool same_frac {false};
//
//    Fraction frac{};
//
//    Fraction frc {1};
//
//    int count = 1;
//    while (!(!frac2)) {
//        if (count >= 2 && frac1 == frac2){
//            same_frac = true;
//            break;
//        }
//        std::cout << "Here is the fraction you just entered: " << frac2 << "\n";
//        frac1 = Fraction{frac2};
//        std::cin >> frac2;
//        count ++;
//    }
//    if (same_frac) {
//        std:: cout << "You entered the same fraction twice in a row " << frac1 << "\n";
//    }
//    else {
//        std::cout << "You entered zero " << frac2 << "\n";
//    }
//}


void test_bst(){
    Node* n20 = new Node(20);
    Node* n10 = insertNode(n20, 10);
    Node* n27 = insertNode(n20, 27);
    Node* n25 = insertNode(n10, 15);
    Node* n5 = insertNode(n10, 5);
    Node* n22 = insertNode(n27, 22);

    inorderTraversal(n20);

    for (int i = 0; i < 10; i ++ ){
        int x;
        std::cin >> x;
        n20 = deleteNode(n20, x);
        std::cout << "\nafter deleting " << x << '\n';
        inorderTraversal(n20);
    }
//

    freeBSTMemory(n20);
}


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

void arrayListFunction() {
    ArrayList<double> myArrayList {1, 2};
    for (int i = 0; i < 10; i++) {
        myArrayList.add(i);
        std::cout << "adding " << i << " to the list\n";
        std::cout << myArrayList << "\n";
    }
//    std::cout << "\n";
//    std::cout << myArrayList << "\n";

    int s = myArrayList.size();

    std:: cout << "the length of the list is " << s << "\n";

    for (int i = 0; i < 5; i++) {
        myArrayList.addAt(std::pow(i, 2), i);
        std::cout << "attempting to add " << std::pow(i, 2) << " at position " << i << "\n";
        std::cout << myArrayList << "\n";
    }
//

    std::cout << "the length of this list at this point is " << myArrayList.size() << "\n";

    for (int i = 0; i < 5; i++) {
        std:: cout << "attempting to remove the element at position " << i << "\n";
        myArrayList.removeAt(i);
        std::cout << myArrayList << "\n";
    }

    std::cout << "the length of this list at this point is " << myArrayList.size() << "\n";

    // seed the random generator
    srand(0);

    for (int i = 0; i < 5; i++) {
        int value{mod(rand(), 10)};
        std::cout << "attempting to remove " << value << "\n";
        myArrayList.remove(value);
        std::cout << myArrayList << "\n";
    }

}


void oop_custom_containers() {
    ArrayList<double> l1 {3};
    DoubleLinkedList<double> l2 {1};
    std::vector<List<double>*> vec_lists {&l1, &l2};

    for (auto c : vec_lists) {
        std::cout << c ->size() << "\n";
        for (int i = 0; i < 5; i ++) {
            c ->add(i);
        }
        std::cout << c -> size() << "\n";
    }

    for (auto c: vec_lists) {
        std:: cout << *c << "\n";
    }

    // if the 'get' function is made to return by reference instead of value
    // then uncomment the few lines below to

//    for (auto c: vec_lists){
//        std::cout << "before assignment: " << c -> get(0) << "\n";
//        double& val{c -> get(0)};
//        val = 10;
//        std::cout << "after assignment: " << c -> get(0) << "\n";
//
//    }

}


# include <vector>
# include <utility>
void some_function() {
    std::vector<std::string> v {"a", "b", "c"};
    std::string str = {"well"};
    v.push_back(std::move(str));
    std::cout << "the last element of 'v':" << v[static_cast<int>(v.size() - 1)] << "\n";
    std::cout << "the 'str' variable after moving: " << str << "\n";

    // let's do some copying
    std::string str2 = {"well"};
    v.push_back(str2);
    std::cout << "the last element of 'v':" << v[static_cast<int>(v.size() - 1)] << "\n";
    std::cout << "the 'str2' variable after usual assignment: " << str2 << "\n";
}

# include<memory>
void unique_pointers() {
    std::unique_ptr<Fraction> p_frac = std::make_unique<Fraction>(3, 4);
    std::unique_ptr<std::vector<int>> p_vec = std::make_unique<std::vector<int>>(4);
    // the syntax is as follow: std::make_unique <Type> (*constructor args)
    std::unique_ptr<std::string> p_string = std::make_unique<std::string>("ayhembouabid", 0, 5);

    std::unique_ptr<Fraction> p1 {new Fraction()};
    std::unique_ptr<Fraction> p2 {}; // always set with {} not nullptr

    // assignment is disabled; which makes sense ...
    p2 = std::move(p1);

    if (p1 == nullptr) {
        std::cout << "p1 after move is nullptr\n";
    }

    std::cout << *p2 << "\n";

    std::cout << *p_frac << "\n";
    std::cout << *p_string << "\n";

}

# include "GeneralProgramming/iterators.h"

//void play_with_iterators() {
//    // let's make an array of Fractions
//    Fraction* frs = new Fraction[4];
//    for (int i = 0; i < 4; i ++) {
//        frs[i] = Fraction(2, 7);
//    }
//    int num_frac = count(frs, frs + 4, Fraction{2, 7});
//    std::cout << num_frac << "\n";
//    delete[] frs;
//}

