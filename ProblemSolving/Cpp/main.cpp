# include <iostream>
# include "arrays/searching.h"
# include "trees/file1.h"
# include "trees/file2.h"
# include "dp/dp1.h"
# include "backtracking/bt1.h"
# include <cassert>
# include <functional>
# include <numeric>
# include <string>
# include <cstdlib>
# include "utils.h"

# include "arrays/dequeue.h"
# include "arrays/hash_map_set.h"

void trees_f() {
    Node n1(1);
    Node n2(2);
    Node n3(3);
    Node n4(4);
    Node n5(5);
    Node n6(6);
    Node n7(7);
    Node n8(8);
    Node n9(9);
    Node n10(10);
    Node n11(11);
    Node n12(12);
    Node n13(13);

    n1.left = &n2;
    n1.right = &n3;

    n2.left = &n4;
    n2.right = &n5;

    n3.left = &n6;
    n3.right = &n7;

    n6.left = &n8;
    n6.right = &n9;

    n9.left = &n10;
    n10.right = &n11;

    int v1= 2, v2 = 2;

    auto pair_res = lca_distance(&n1, v1, v2);

    Node* res = pair_res.first;

    int d1 = pair_res.second.first, d2 = pair_res.second.second;

    int d = findDist(&n1, v1, v2);

    if (res != nullptr) {
        std::cout << "LCA: " << res -> data << "\n";
        std::cout << "distance to " << v1 << " : " << d1 << " and distance to " << v2 << " : " << d2 << "\n";

        std::cout << "Distance between " << v1 << " and " << v2 << " : " << d << "\n";
    }
    else {
        std::cout << "no common ancestor";
    }


//    for (int v : res) {
//        std::cout << v << " ";
//    }
    std::cout << "\n";
}
void bst_f() {

    Node n1(2);
    Node n2(1);
    Node n3(5);
    Node n4(20);
    Node n5(40);
    Node n6(4);
//    Node n6(12);
    Node n7(7);
//    Node n8(9);
//    Node n9(12);

    n1.left = &n2;
    n1.right = &n3;
//    n2.left = &n4;
//    n2.right = &n5;
    n3.left = &n6;
    n3.right = &n7;
//    n4.right = &n5;
//    n5.right = &n6;
//    n5.right = &n8;


    auto newRoot = modify(&n1);

    std::vector<int> values  {};

    inorderTraversal(newRoot, values);

    for (int v: values) {
        std::cout << v << " ";
    }
    std::cout << "\n";
}

void some_dp1() {
std::vector<int> arr = {2, 3, 5, 10, 22, 24, 30, 1};
auto subsets = allSubsets(arr);
std::vector<int> sums = {};
for (auto & s: subsets) {
    if (s.size() == 0){continue;}
    sums.push_back(std:: accumulate(s.begin(), s.end(), 0));
}

for (int s = 1; s <= 200; s++) {
    bool res = isSubsetSum(arr, s);
    assert(res == (std::count(sums.begin(), sums.end(), s) >= 1));}
}

void dpf() {
    std::string s1 {"acaab"};
    std::string s2 {"aa"};

    std::cout << numDistinct(s1, s2) << "\n";
}


void array_function() {

    // some very basic array set problem

    // vi a {5, 4, 3, 3, 1, 1, 2, 1};
    // vi res = removeDuplicate(a);
    // for (const int v : res) {
    //     std::cout << v << " ";
    // }
    // std::cout << std::endl;

    // some interesting search problem
    int a[] = {1, 1, 2, 2, 3, 3, 4};
    int n1 = sizeof(a) / sizeof(a[0]);
    std::cout << search(n1, a) << "\n";

    int b[] = {1, 2, 2, 3, 3};
    int n2 = sizeof(b) / sizeof(b[0]);
    std::cout << search(n2, b) << "\n";


    int c[] = {1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 7};
    int n3 = sizeof(c) / sizeof(c[0]);
    std::cout << search(n3, c) << "\n";

    int d[] = {1, 1, 2, 3, 3};
    int n4 = sizeof(d) / sizeof(d[0]);
    std::cout << search(n4, d) << "\n";
}


int main() {
    array_function();
}

