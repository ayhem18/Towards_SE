#ifndef LEARNC___ITERATORS_H
#define LEARNC___ITERATORS_H

template <typename T>
class ImmutableIterator {
public:
    // the immutable iterator should not modify the underlying data structure
    // hence the '*' operator returns by value and not by reference
    virtual T operator * () const = 0;
    virtual bool operator == (const ImmutableIterator& another) const = 0;
    virtual bool operator != (const ImmutableIterator& another) const = 0;
};


template <typename T>
class ImmutableUniDirIterator: public ImmutableIterator<T> {
public:
    virtual ImmutableUniDirIterator& operator ++(int) = 0;
};


template <typename T>
class ImmutableBiDirIterator: public ImmutableIterator<T> {
public:
    virtual ImmutableBiDirIterator& operator ++(int) = 0;
    virtual ImmutableBiDirIterator& operator --(int) = 0;
};

template <typename T>
class MutableIterator {
public:
    // the mutable iterator should be able to modify the data structure
    // hence the '*' operator returns by reference
    virtual T& operator * () = 0;
    virtual bool operator == (const MutableIterator& another)  = 0;
    virtual bool operator != (const MutableIterator& another)  = 0;
};

template <typename T>
class MutableUniDirIterator: public MutableIterator<T> {
public:
    virtual MutableUniDirIterator& operator ++(int)  = 0;
};

template <typename T>
class MutableBiDirIterator: public MutableIterator<T>{
public:
    virtual MutableBiDirIterator<T>& operator ++(int) = 0;
    virtual MutableBiDirIterator& operator --(int) = 0;
};

#endif //LEARNC___ITERATORS_H
