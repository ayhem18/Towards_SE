#ifndef LEARNC___TREE_H
#define LEARNC___TREE_H

template <typename T>
class BTreeNode{
public:
    T data;
    BTreeNode<T>* left;
    BTreeNode<T>* right;
    explicit BTreeNode(int val) {
        this -> data = val;
        this -> left = nullptr;
        this -> right = nullptr;
    }
};

template <typename T>
class BTree {
protected:
    int m_size;
    explicit BTree(int size): m_size(size) {};
public:
    virtual void add(const T& element) = 0;
    virtual void remove(const T& element) = 0;
    virtual int depth() const = 0;
    int size() const {
        return m_size;
    }
};




#endif //LEARNC___TREE_H
