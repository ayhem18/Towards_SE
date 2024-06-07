#ifndef LEARNC___ITERATORS_H
#define LEARNC___ITERATORS_H


//template <typename T>
//concept isEqual = requires(T a, T b) {
//    a == b;
//    a != b;
//};
//
//template <typename T, typename P>
//concept T_reference = requires(P p) {{*p} -> std::convertible_to<T>;};
//
//template <typename P>
//concept Incremental = requires(P p) {p ++;};
//
//template <typename T, typename P>
//int count(P begin, P end, const T& element) requires T_reference<T,P> && Incremental<P> && isEqual<T> {
//    T* traverse = begin;
//    int count {0};
//    while (traverse != end) {
//        count += (*traverse == element);
//        traverse ++;
//    }
//    return count;
//}

#endif //LEARNC___ITERATORS_H
