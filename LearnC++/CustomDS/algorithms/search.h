// #ifndef LEARNC___SEARCH_H
// #define LEARNC___SEARCH_H
// #include <concepts>

// template <typename T>
// concept isEqual = requires(T a, T b) {
//     a == b;
// };

// template <typename T, typename P>
// concept T_reference = requires(P p) {{*p} -> std::convertible_to<T>;};

// template <typename P>
// concept Incremental = requires(P p) {p ++;};

// template <typename T, typename P>
// int count(P begin, P end, const T& element) requires Incremental<P> && isEqual<T> {
//     P traverse = begin;
//     int count {0};
//     while (traverse != end) {
//         count += (*traverse == element);
//         traverse ++;
//     }
//     return count;
// }

// #endif //LEARNC___SEARCH_H
