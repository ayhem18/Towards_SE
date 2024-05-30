#ifndef LEARNC___OBJECTS_H
#define LEARNC___OBJECTS_H

# include <algorithm>
# include <iostream>
# include <set>
#include <utility>
#include <cassert>

// let's create a Box class
class Box {
private:
    double m_length;
    double m_width;
    double m_height;
public:
    Box(double length, double width, double height): m_length(std::max(length, width)),
    m_width(std::min(length, width)), m_height(height) {};
    // copy constructor
    Box(const Box& anotherBox): Box(anotherBox.m_length, anotherBox.m_width, anotherBox.m_height) {
        std::cout << "Calling the copy operator \n";
    };

    // conversion constructor
    Box(double height): Box(1, 1, height) {};

    double getVolume() const {
        return m_length * m_height * m_width;
    }

    // comparison operators
    bool operator > (Box& another) const{
        return getVolume() > another.getVolume();
    }
    bool operator >= (Box& another) const {
        return getVolume() >= another.getVolume();
    }
    bool operator < (Box& another) const{
        return getVolume() < another.getVolume();
    }
    bool operator <= (Box& another) const{
        return getVolume() <= another.getVolume();
    }
    bool operator == (Box& another) const {
        // create a set of object
        std::set<double> all_sides {m_width, m_height, m_length, another.m_length, another.m_width, another.m_height};
        return all_sides.size() <= 4;
    }

    // let's implement the * operator
    Box operator * (double scale) const{
        return {m_length * scale, m_width * scale, m_height * scale};
    }

    // let's implement the assignment operator
    Box& operator = (const Box& anotherBox) {
        // set the values here
        m_width = anotherBox.m_width;
        m_length = anotherBox.m_length;
        m_height = anotherBox.m_length;
        std::cout << "calling the '=' operator" << "\n";
        return *this;
    }



    friend std::ostream& operator << (std::ostream& out, const Box& box);
};


// classes for the SSAD course 3rd week
class Animal {
protected:
    const std::string m_name {};
    int m_age {};
public:
    // constructor
    Animal(std::string name, int age): m_name{std::move(name)}, m_age{age} {} ;

    const std::string &getName() const {
        return m_name;
    }

    int getAge() const {
        return m_age;
    }

    void setAge(int mAge) {
        m_age = mAge;
    }

    // pure virtual function
    virtual std::string make_sound() const = 0;
};

class LandAnimal: public Animal {
public:
    LandAnimal(const std::string& name, int age): Animal(name, age) {};
    // override the make_sound method
    std::string make_sound() const override {
        return "land sounds";
    }
    virtual void walk() const = 0;
};

class WaterAnimal: public Animal {
public:
    WaterAnimal(const std::string& name, int age): Animal(name, age) {};
    // override the make_sound method
    std::string make_sound() const override {
        return "water sounds";
    }
    virtual void swim() const = 0;
};

class Lion: public LandAnimal {
public:
    Lion(const std::string& name, int age): LandAnimal(name, age) {};
    void walk() const override {
        std::cout << "a lion walking" << "\n";
    }
    std::string make_sound() const override {
        return  "Lion Roaring";
    }
};

class Dolphin: public WaterAnimal {
public:
    Dolphin(const std::string& name, int age): WaterAnimal(name, age) {};
    void swim() const override {
        std::cout << "a dolphin swimming" << "\n";
    }
    std::string make_sound() const override {
        return  "Dolphin cute sounds";
    }
};

std::ostream& operator << (std::ostream& out, Animal& a);

// classes for the SSAD course 4th week
class Account {
protected:
    const int account_number {};
    double balance {};
    const std::string owner_name {};

    // make the constructor protected
    Account(int ac_number, double initial_balance, std::string owner_name):
    account_number{ac_number}, balance(initial_balance), owner_name{std::move(owner_name)} {
        // make sure the initial balance is non-negative
        assert(initial_balance >= 0.0);
    }
public:
    // disable the copy constructor
    Account(Account& anotherAcc) = delete;
    Account& operator = (const Account& anotherAccount) = delete;

    const std::string &getOwnerName() const {
        return owner_name;
    }

    int getAccountNumber() const {
        return account_number;
    }

    double getBalance() const {
        return balance;
    }

    void deposit(double money){
        balance += money;
    }

    void withdraw(double money){
        assert (money <= balance);
        balance -= money;
    }
};

class SavingAccount: public Account {
protected:
    double interest_rate {};
public:
    SavingAccount(int ac_number, double initial_balance, const std::string& owner, double rate):
            Account(ac_number, initial_balance, owner), interest_rate{rate} {};

};
#endif //LEARNC___OBJECTS_H
