#ifndef LEARNC___LIST_H
#define LEARNC___LIST_H
# include <iostream>

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

// let's define a struct for the DLL to use

template <typename T>
class DLLNode {
public:
    T val;
    DLLNode<T> *next {nullptr};
    DLLNode<T> *previous {nullptr};
    DLLNode(T val, DLLNode* n, DLLNode*prev): val{val}, next{n}, previous{prev} {};
    // calling the 3 argument constructor
    // either specify both next and previous nodes or none of them
    explicit DLLNode(T val): DLLNode(val, nullptr, nullptr) {};
};

//template <typename T>
//class DoubleLinkedList: public List<T> {
//public:
//    // let's define the functions we need to have
//    virtual void add(const T& new_element) {
//        this -> m_size += 1;
//    };
//
//    virtual void addAt(const T& new_element, int index) {};
//
//    virtual void remove(const T& element) {};
//
//    virtual void removeAt(int index) {};
//};

template <typename T>
class DoubleLinkedList: public List<T> {
private:
    // the head
    DLLNode<T>* head {nullptr};
    // the tail
    DLLNode<T>* tail {nullptr};

public:
    explicit DoubleLinkedList(T val):
            List<T>(1), head{nullptr}, tail{nullptr} {
        this -> head = new DLLNode(val);
        this -> tail = head;
    }
    DoubleLinkedList():List<T>{}, head{nullptr}, tail{nullptr} {};

    // let's create the destructor
    ~DoubleLinkedList() {
        // create some traverse node
        DLLNode<T>* traverse_node = head;
        while (traverse_node != nullptr) {
            DLLNode<T>* next = traverse_node -> next;
            free(traverse_node);
            traverse_node = next;
        }
    }

    void add(const T& val) override {
        // start with the simple case, if the list is empty
        if (this -> m_size == 0) {
            this -> head = new DLLNode<T>(val);
            this -> tail = head;
        }

            // if there is only one element
        else if (this -> m_size == 1) {
            auto * new_node = new DLLNode<T>(val, nullptr,  head);
            head -> next = new_node;
            tail = new_node;
        }

        else {
            // create a new node
            auto * new_node = new DLLNode<T>(val, nullptr,  tail);
            // link the tail to the new node
            tail -> next = new_node;
            tail = new_node;
        }

        // regardless increase the size
        this -> m_size += 1;
    }

    void remove(const T& val) override {
//        // if the list is empty:
//        if (this->m_size == 0) {
//            return;
//        }
//        if ((this->m_size == 1) && (head->val == val)) {
//            // at this point
//            head = nullptr;
//            tail = nullptr;
//            this->m_size = 0;
//        }
//        // we have at least 2 elements in the list: head and tail are supposedly different
//        DLLNode<T> *traverse_node = head;
//        while ((traverse_node != nullptr) && (traverse_node->val != val)) {
//            traverse_node = traverse_node->next;
//        }
//        if (traverse_node == nullptr) {
//            // the element to be removed was not found here, abort
//            return;
//        }
//
//        // at this point, we know the element was found
//        // reduce the size
//        this->size--;
//        // 2 operations to be done: for the next of traverse node: set the 'previous'
//        // for the 'previous' of traverse_node set the 'next'
//        DLLNode<T> *prev = traverse_node->previous;
//        DLLNode<T> *next = traverse_node->next;
//
//        // 2 things can go wrong here: previous is null: meaning, we are dealing with the head
//        if (prev == nullptr) {
//            head = next;
//            free(traverse_node);
//            return;
//        }
//
//        // if next is null, then we are dealing with the tail of the list
//        if (next == nullptr) {
//            // the 'prev' node should point to null now
//            prev->next = nullptr;
//            tail = prev;
//            free(traverse_node);
//            return;
//        }
//
//        // we are neither at the head nor the tail
//        prev->next = next;
//        next->previous = prev;
//        free(traverse_node);
    }

    void addAt(const T& val, int index) override{
//        // the index cannot be larger than the current size or less than 0
//        assert((index >= 0) && (index <= this -> m_size) &&
//               "the index should be larger than 0 and less than " + static_cast<std::string>(this -> m_size) + ". Found " + static_cast<std::string>(this -> index));
//
//
//        // create the new node
//        auto* new_node = new DLLNode<T> {val};
//
//        // consider the case of the head
//        if (index == 0) {
//            // set the next pointer to the current head
//            new_node -> next = this -> head;
//            this -> head -> previous = new_node;
//            // set the head to the new node
//            this -> head = new_node;
//            // increase the size
//            this -> m_size += 1;
//
//            return;
//        }
//
//        DLLNode<T> traverse_node = this -> head;
//        int count = 0;
//        while (count < index - 1) {
//            count ++;
//            traverse_node = traverse_node -> next;
//        }
//        // at this point the 'traverse_node' is at the 'index - 1' position.
//        new_node -> next = traverse_node -> next;
//        new_node -> previous = traverse_node;
//
//        traverse_node -> next -> previous = new_node;
//        traverse_node -> next = new_node;
//
//        if (index == this -> m_size) {
//            // modify the tail if the element is added to the end of the list
//            this -> tail = new_node;
//        }
//
//        // increase the size
//        this -> m_size += 1;
    }

    void removeAt(int index) override {
//        // the index cannot be larger than the current size or less than 0
//        assert((index >= 0) && (index < this -> m_size) &&
//               "the index should be larger than 0 and less than " + static_cast<std::string>(this -> m_size) + ". Found " + static_cast<std::string>(this -> index));
//
//        // consider the case of the head
//        if (index == 0) {
//            DLLNode<T> new_head = (this -> head) -> next;
//            new_head -> previous = nullptr;
//            // free the previous head
//            free(this -> head);
//            this -> head = new_head;
//
//            // decrease the size
//            this -> m_size -= 1;
//
//            return;
//        }
//        // let's consider other cases
//        auto traverse_node = this -> head;
//
//        int count = 0;
//        while (count < index - 1) {
//            count ++;
//            traverse_node = traverse_node -> next;
//        }
//
//        // at this point the 'traverse_node' is at the 'index - 1' position
//        DLLNode<T> new_next_node = traverse_node -> next -> next;
//        new_next_node -> previous = traverse_node;
//        free(traverse_node -> next);
//        traverse_node -> next = new_next_node;
//
//        if (index == this -> m_size - 1) {
//            // modify the tail if the element is added to the end of the list
//            this -> tail = traverse_node;
//        }
//
//        // decrease the size
//        this -> m_size -= 1;
    }
    // let's create a friend function to display the content of the linked list
    friend std::ostream& operator << (std::ostream& out, const DoubleLinkedList<T>& list)
    {
// let's start with the head
        if (list.size() == 0) {
            out << "The list is empty";
            return out;
        }

        DLLNode<T>* traverse_node = list.head;
// first display the value at the head
        out << traverse_node -> val;
        traverse_node = traverse_node -> next;
        while (traverse_node != nullptr) {
            out << "-->" << traverse_node -> val;
            traverse_node = traverse_node -> next;
        }
        return out;
    }

};


#endif //LEARNC___LIST_H
