#include <iostream>
# include <string>
#ifndef LEARNC___OOP_STARTER_H
#define LEARNC___OOP_STARTER_H

struct IntPair {
    // public by default
    int p1;
    int p2;
    void print() {
        std::cout << "int 1: " << p1 << " int 2: " << p2 << "\n";
    }
    bool isEqual(IntPair another) {
        return ((another.p1 == p1) && (another.p2 == p2)) || ((another.p1 == p2) && (another.p2 == p1));
    }
};


class clsWithConstant {
private:
    int val = 1; // one best practice is to have private fields preceded by "m"
    std::string s;
public:
    // let's define a constructor the right way

    clsWithConstant(int v, const std::string& s): val{v}, s{s}
    {
    }

//    clsWithConstant(int v, std::string& s)
//    {
//        this -> val = v;
//        this -> s = s;
//    }


    clsWithConstant() {
        this -> val = 1;
        this -> s = "";
    }

    void // return type
    const_function() // function name and arg types
    const // add 'const' if the function is constant

    // constant objects cannot call non-constant methods
    // of course if this function was to assign a value to 'val', then it wouldn't compile
    {
        std::cout << this -> val;
    }

    // one huge misconception apparently is that private fields are available on instance level whereas they are
    // available on a class level
    void access_other_obj_private(const clsWithConstant &another) const {
        std:: cout << "Here I am accessing the private field of the other object " << another.val << " see ? \n";
    }

    std::string& getS() {
        return this -> s;
    }

    void function_with_s() {
        this -> s.insert(0, "aa");
    }
};


class Ball {
private:
    // preferably provide default values for data members !!!
    double m_radius {1.0};
    std::string m_color {"transparent"};
public:
//    Ball(double radius, std::string_view color) : m_radius(radius), m_color(color)
//    {
//        std::cout << "constructor called" << "\n";
//    }
//
//    Ball(double rad):
//    // delegating to the constructor above
//    Ball(rad, "transparent")
//    {
//
//    };
//
//    Ball(): Ball(1.0, "transparent") {} ;

//    // the commented code above can be replaced with:
//    Ball(double radius = 1.0, std::string_view color = "transparent") : m_radius(radius), m_color(color)
//    {
//        std::cout << "constructor called" << "\n";
//    }

    // let's do some weird stuff: answering the question at the end of the page:
    // https://www.learncpp.com/cpp-tutorial/delegating-constructors/
    Ball(double radius = 10.0, const std::string_view& color = "Black"): m_radius(radius), m_color(color){
//        std::cout << "Ball(" << m_color << ", " << m_radius << ") constructed" << "\n";
    };

    Ball(const std::string_view& color, double radius = 10.0): Ball(radius, color){};

    // let's create a copy constructor
    // the implicit copy constructor meets most needs...
    Ball(const Ball& another_ball): Ball(another_ball.m_radius, another_ball.m_color) {
        std::cout << "the copy constructor called" << "\n";
    }

    // getters
    const std::string& getColor() const{
        return this -> m_color;
    }

    double getRadius() const{
        return this -> m_radius;
    }

    // it is possible to define functions that accept class as argument
    // however if we have constructors (type) then we can ass the "type" to such functions
    // and the code will compile

};


void print_ball(const Ball ball_obj);
//void print_ball(const Ball& ball_obj);

#endif