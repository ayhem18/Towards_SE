// this file contains the implementation of a generic ArrayList
#ifndef LEARNC___ARRAYLIST_H
#define LEARNC___ARRAYLIST_H

# include "list.h"
# include <cassert>
#include <algorithm>

template <typename T>
class ArrayList: public List<T> {
private:
    inline static int DEFAULT_INITIAL_CAPACITY {8};
    int capacity {DEFAULT_INITIAL_CAPACITY};
    // dynamically allocated memory for the initial value
    T* array; // = new T[DEFAULT_INITIAL_CAPACITY];

    // let's define a function to reallocate memory
    void reallocate() {
        // define the new capacity as twice the current capacity
        int new_capacity = 2 * capacity;
        // first allocate memory for the new array
        T* new_array = new T[new_capacity];

        // copy the first m->size elements to the new array
        for (int i = 0; i < this -> m_size; i ++) {
            new_array[i] = array[i];
        }

        // free the old array
        delete [] array;

        // make sure to set the 'array' field to the new one
        array = new_array;
        // and update the capacity field
        capacity = new_capacity;
    }

public:
    ArrayList():List<T>{}, capacity {DEFAULT_INITIAL_CAPACITY}{
        array = new T[DEFAULT_INITIAL_CAPACITY];
    };

    explicit ArrayList(T val): ArrayList(val, ArrayList::DEFAULT_INITIAL_CAPACITY) {};

    ArrayList(T val, int initial_capacity): List<T>{1}, capacity(initial_capacity) {
        assert(initial_capacity > 0 && "The internal array must have a non-negative capacity");
        // allocate the memory according to the initial capacity
        array = new T[initial_capacity];
        // set the first element to 'val'
        array[0] = val;
    };

    ~ ArrayList() {
//         the main idea here is free all the memory currently allocated by the object
        std::cout << "\ncalling the ArrayList destructor\n";
        delete [] array;
    }

    // let's override some methods
    void add(const T& val) override;

    void remove(const T& val) override;

    void addAt(const T& val, int index) override;

    void removeAt(int index) override;

    T get(int index) const override {
        std::cout << "\nThe ArrayList class calling the 'get' function with index " << index << "\n";
        // use the [] operator (keep in mind that [] returns a reference)
        // so save it to a local
        assert((index >= 0 && index < this -> m_size) && "the index should be larger than 0 and less or equal to the size of the list");
        return array[index];
    }

    // implement the subscript operator
    T& operator [] (int index) {
        assert((index >= 0 && index < this -> m_size) && "the index should be larger than 0 and less or equal to the size of the list");
        return array[index];
    }

    friend std::ostream& operator << (std::ostream& out, ArrayList<T> list) {
        out << "\n the ArrayList implementation of <<\n";
        if (list.size() == 0) {
            out << "The list is empty";
            return out;
        }
        for (int i = 0; i < list.size() - 1; i ++) {
            out << list.array[i] << " ";
        }
        out << list.array[list.size() - 1];
        return out;
    };

};


template<typename T>
void ArrayList<T>::add(const T& val) {
    // the first step is to check whether the number of elements will exceed the capacity
    // after the addition or not
    if ((this -> m_size + 1) > capacity) {
        reallocate();
    }
    // set the value
    array[this -> m_size] = val;
    // increase the size
    this -> m_size ++;
}

template<typename T>
void ArrayList<T>::addAt(const T &val, int index) {
    // make sure the index fits
    assert((index >= 0) && (index <= this -> m_size) && "the index should be larger than 0 and less or equal to the size of the list");

    // check the capacity thingy
    if ((this -> m_size + 1) > capacity) {
        reallocate();
    }
    for (int x = this -> m_size - 1; x >= index; x--) {
        // shift all the elements to the right
        array[x + 1] = array[x];
    }
    // set the value at the correct index
    array[index] = val;
    this -> m_size ++;
}

template<typename T>
void ArrayList<T>::remove(const T &val) {
    // iterate until you find it
    for (int x = 0; x < this -> m_size; x ++) {
        if (array[x] == val) {
            removeAt(x);
            break;
        }
    }
}

template<typename T>
void ArrayList<T>::removeAt(int index) {
    assert((index >= 0) && (index < this -> m_size) && "the index should be larger than 0 and less or equal to the size of the list");
    // shift all elements to the left
    for (int x = index + 1; x < this -> m_size; x++) {
        array[x - 1] = array[x];
    }
    // make sure to update the size
    this -> m_size --;
}


#endif //LEARNC___ARRAYLIST_H
