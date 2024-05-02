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
    void f() const{
        std::cout << "I am a fruit " << "\n";
    }
    const std::string m_name {};
    const std::string m_color {};
public:
    Fruit(const std::string_view& name, const std::string_view& color): m_name(name), m_color(color) {};

    const std::string& getName() {
        return m_name;
    }

    const std::string& getColor() {
        return m_color;
    }
};

class Apple: public Fruit {
private:
    const float fibers_per_g {};
public:
    Apple(const std::string_view& name,
          const std::string_view& color,
          float fibers_per_g):
        Fruit(name,color), fibers_per_g(fibers_per_g)
        {
        };
    int getFiberPerG() const {
        return fibers_per_g;
    }
};

class Banana: public Fruit {
public:
    Banana(const std::string_view& name,
          const std::string_view& color):
          Fruit(name,color)
        {
        };

    void f() const {
        Fruit::f();
        std::cout << "I am a banana" << "\n";
    }
};

#endif //LEARNC___OOP_INHERITANCE_H
