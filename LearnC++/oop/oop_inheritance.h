#ifndef LEARNC___OOP_INHERITANCE_H
#define LEARNC___OOP_INHERITANCE_H

# include <string>
# include <iostream>

class Person {
protected:
    std::string m_name {};
public:
    // explicit avoid non explicit conversion
    explicit Person(const std::string_view& name): m_name{name} {};
    const std::string& getName() {
        return m_name;
    }
};

//
class HighSchoolStudent : public Person{
protected:
    int grade = {11};
public:
    HighSchoolStudent(const std::string_view& name, int grade): Person(name), grade{grade} {
    }
    void greet() {
        std::cout << "Hello My name is " << m_name;
    }
};

// let's write some silly classes
class Fruit {
protected:
    const std::string m_name {};
    const std::string m_color {};
public:
    Fruit(const std::string_view& name, const std::string_view& color): m_name(name), m_color(color) {};

    const std::string& getName() const{
        return m_name;
    }

    const std::string& getColor() const {
        return m_color;
    }
    void some_funct() const {
        std::cout << "I am  a fruit " << "\n";
    }

    // friend functions are not inheritable !!!
    // so if the derived wants to call a friend function, then it can convert the object
    // to the base clas using static_cast<BaseClass> and use the friend function with the cast object
};

class Apple: public Fruit {
private:
    const float fibers_per_g{};
public:
    Apple(const std::string_view &name,
          const std::string_view &color,
          float fibers_per_g) :
            Fruit(name, color), fibers_per_g(fibers_per_g) {};

    float getFiberPerG() const {
        return fibers_per_g;
    }
    // for some reason we do not want users to access the some_funct through the Apply objects
    //    void some_funct() const {
////        Fruit:: some_funct();
//        std::cout << "More specifically, I am an apple" << "\n";
//    }



// make the some_funct method private
// private:
//    using Fruit::some_funct;

// we can even make certain methods completely inaccessible
    void some_funct() const = delete;
//    void another_func() const {
//        // this means we cannot access this function whatsoever, even inside the class itself
            // the compiler will complain about this method, so it is commented
//        some_funct();
//    }
};

//overloading the << operator for the Apple class
std::ostream& operator << (std::ostream& out, const Apple & a) {
    out << "Banana("<< a.getName() << "," <<a.getColor() << "," << a.getFiberPerG() << ")";
    return out;
}


class Banana: public Fruit {
public:
    Banana(const std::string_view& name,
          const std::string_view& color):
          Fruit(name,color)
        {
        };

//    void some_funct() const {
////        Fruit:: some_funct();
//        std::cout << "More specifically, I am a banana" << "\n";
//    }
};

// overloading the << operator for the Banana class
std::ostream& operator << (std::ostream& out, const Banana & b) {
    out << "Banana("<< b.getName() << "," <<b.getColor() << ")";
    return out;
}

#endif //LEARNC___OOP_INHERITANCE_H
