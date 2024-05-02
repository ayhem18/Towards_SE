// This script contains the implementation of the classes introduced by the assignment

#ifndef LEARNC___CLASSES_H
#define LEARNC___CLASSES_H

# include <string>

class classes {
// TODO: make this class abstract !!! (or an interface)
protected: // protected since it is expected that the classes will be extended by other derived classes
    int m_id {};
public:
    explicit classes(int id): m_id(id) {

    };

    int getId() const {
        return m_id;
    }
};

class Car: public classes {
public:
    explicit Car(int id): classes(id){};
};


class Person: public classes{
protected:
    const std::string m_name {};
    const std::string m_gender {}; // TODO: make it an enumerate !!!

public:
    Person(int id, const std::string_view& name, const std::string_view & gender):
            classes(id), m_name{name}, m_gender{gender} {};

    const std::string& getName() {
        return m_name;
    };

    const std::string& getGender() {
        return m_gender;
    };
};

// the final class is the Transformer
class Transformer: public Person {
public:
    Transformer(int id, const std::string_view& name, const std::string_view & gender):
            Person(id, name, gender) {};
};


#endif //LEARNC___CLASSES_H
