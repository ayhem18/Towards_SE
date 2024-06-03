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
    List(): List{0} {};

public:

    int size() const {
        return m_size;
    }
    // let's define the functions we need to have
    virtual void add(const T& new_element) = 0;

    virtual void addAt(const T& new_element, int index) = 0;

    virtual void remove(const T& element) = 0;

    virtual void removeAt(int index) = 0;

    virtual T get(int index) const = 0;

    // define a virtual destructor since we will be used some non-trivial destruction process
    virtual ~List() = default;

    friend std::ostream& operator <<(std::ostream& out, const List<T>& list){
        // a default implementation of the << operator
        out << "\nthe default implementation of << operator\n";
        if (list.m_size == 0) {
            out << "The list is empty";
            return out;
        }

        for (int i = 0; i < list.m_size - 1; i ++ ){
            out << list.get(i) << " ";
        }
        out << list.get(list.m_size - 1);
        return out;
    };
};



#endif //LEARNC___LIST_H
