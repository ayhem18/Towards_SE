#include <iostream>
# include "arrays/searching.h"
# include "trees/file1.h"
# include "trees/file2.h"
# include "dp/dp1.h"
# include "backtracking/bt1.h"
# include <cassert>
#include <functional>
#include <numeric>
# include "utils.h"

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

//    for (int j = 1; j <= 20; j++) {
//        auto v = printNearNodes(&n1, 1, j);
//        std::cout << "the elements in the range " << 1 << " " << j << " are:\n";
//        for (int i: v) {
//            std::cout << i << " ";
//        }
//        std::cout << "\n";
//    }

}

void some_dp1() {
//    for (int i = 1000; i < 1005; i++) {
//        std::cout << "index: " << i << " bottom up: " << bottomUp(i) << ", topdown: " << topDown(i) << "\n";
//    }
//
////    std::cout << "index: " << i << " bottom up: " << bottomUp(i) << ", topdown: " << topDown(i) << "\n";

int coins1[] = {4, 3, 2, 1};
int coins2[] = {1, 2, 3, 4};
std::vector<int> arr = {2, 3, 5, 10, 22, 24, 30, 1};

auto subsets = allSubsets(arr);

std::vector<int> sums = {};
for (auto & s: subsets) {
    if (s.size() == 0){continue;};
    sums.push_back(std:: accumulate(s.begin(), s.end(), 0));
}


for (int s = 1; s <= 200; s++) {
    bool res = isSubsetSum(arr, s);
    assert(res == (std::count(sums.begin(), sums.end(), s) >= 1));
//    std::cout << "sum : " << s << " : " << std::boolalpha << isSubsetSum(arr, s) << "\n";

    //    long long int a1 = count(coins1, 4, s);
//    long long int a2 = count(coins2, 4, s);
//    assert (a1 == a2 && " The values are not the same !!");
}

}

void some_dp2() {
    for (int n = 1; n <= 2000; n++) {
        for (int k = 1; k <= 100; k++) {
            lli r1 = countWays(n, k);
            lli r2 = countWaysDP(n, k);
            assert (r1 == r2 && "The resuls are differnet");
        }
    }

//    int n = 3;
//    for (int j = 1; j <= 4; j++) {
//        std::cout << "ways (" << n << " , " << j << " ) = " << countWays(n, j) <<"\n";
//    }
//    int k = 99999;
//    std::cout << "ways (" << n << " , " << k << " ) = " << countWays(n, k) <<"\n";
}

int main() {
    some_dp2();
}
