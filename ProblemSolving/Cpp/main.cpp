#include <iostream>
# include "arrays/searching.h"
# include "trees/file1.h"
# include "trees/file2.h"
# include "dp/dp1.h"
# include "backtracking/bt1.h"
# include <cassert>
#include <functional>
#include <numeric>
# include "arrays/must_do.h"
# include <string>

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

#include <cstdlib>

void test_subarray_sum() {
    for (int i = 0; i <= 10000; i++) {
        int n = rand() % 10000;
        std::vector<int> arr (n, 0);
        for (int j = 0; j < n; j++) {
            arr[j] = rand() % 1000;
        }
        int s = rand() % 1000;
        auto sol = subarraySum(arr, n, s);
        if (i % 10 == 0) {
            std::cout << "we are at " << i << "\n";
        }

        if (sol[0] != -1) {
            int start = sol[0] - 1, e = sol[1];
            int v = std::accumulate(arr.begin() + start, arr.begin() + e, 0);
            if (v != s) {
                std::cout << "SOMETHING HAPPENED !!!" << "\n";
                break;
            }
        }
    }
}




int main() {
    vi h{1, 2, 3, 5, 8};
    std::make_heap(h.begin(), h.end());
    for (int v : h) {
        std::cout << v<< "\n";
    }
}
