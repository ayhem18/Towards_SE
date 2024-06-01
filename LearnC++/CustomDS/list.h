#ifndef LEARNC___LIST_H
#define LEARNC___LIST_H
# include <iostream>

# include <cassert>

template <typename T>
class List {
protected:
    // this variable stores the number of elements in the list
    int m_size {0};
    // the constructor is made protected so no List object could be created explicitly
    // but can be used by the derived classes
    explicit List(int v): m_size{v} {};

public:
    List(): m_size{0}{};

    int size() const {
        return m_size;
    }
    // let's define the functions we need to have
    virtual void add(const T& new_element) = 0;

    virtual void addAt(const T& new_element, int index) = 0;

    virtual void remove(const T& element) = 0;

    virtual void removeAt(int index) = 0;

    // define a virtual destructor since we will be used some non-trivial destruction process
    virtual ~List() = default;
};



#endif //LEARNC___LIST_H
