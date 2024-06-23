# include "../utils.h"
# include <cmath>
# include <vector>


typedef long long int lli;
typedef std::vector<lli> vll;


/**
 * solve:
 * https://www.geeksforgeeks.org/problems/coin-change2448/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
 */

long long int _count(int coins[], int n, int sum, std::vector<std::vector<long long int>> & memo) {
    if (n <= 0) {
        return 0;
    }

    if (n == 1) {
        return mod(sum, coins[0]) == 0;
    }

    if (sum <= 0) {
        return 0;
    }

    if (memo[n][sum] != -1) {
        return memo[n][sum];
    }

    long long int total = 0;
    int C = coins[n - 1];

    for (int i = 0; i <= sum / C; i++) {
        if (sum == C * i) {
            total += 1;
            continue;
        }
        // this means that sum - C * i > 0
        long long int num_times_without_coins = _count(coins, n - 1, sum - C * i, memo);
        if (num_times_without_coins != 0) {
            total += num_times_without_coins;
        }
    }

    memo[n][sum] = total;
    return total;
}

long long int count(int coins[], int N, int sum) {
    std::vector<std::vector<long long int>>  memo {};
    for (int i = 0;i < N + 1; i++) {
        std::vector<long long int> vector_by_N(sum + 1, -1);
        memo.push_back(vector_by_N);
    }
    return _count(coins, N, sum, memo);
}

/**
 * solve: https://www.geeksforgeeks.org/problems/subset-sum-problem-1611555638/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
 */
bool _isSubsetSum(std::vector<int>&arr, int n, int sum, std::vector<std::vector<int>> & memo){
    if (n == 1) {
        return sum == arr[0];
    }

    if (sum <= 0) {
        return false;
    }

    if (memo[n][sum] != -1) {
        return memo[n][sum];
    }

    if (sum == arr[n - 1]) {
        return true;
    }

    bool res = _isSubsetSum(arr, n - 1, sum - arr[n - 1], memo) || _isSubsetSum(arr, n - 1, sum, memo);
    memo[n][sum] = static_cast<int>(res);
    return res;
}

bool isSubsetSum(std::vector<int>&arr, int sum){
    int N = arr.size();
    std::vector<std::vector<int>>  memo {};
    for (int i = 0;i < N + 1; i++) {
        std::vector<int> vector_by_N(sum + 1, -1);
        memo.push_back(vector_by_N);
    }
    return _isSubsetSum(arr, N, sum, memo);
}


/**
 * solve https://www.geeksforgeeks.org/problems/painting-the-fence3727/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
 */


lli M = static_cast<lli>(pow(10, 9) + 7);

lli f(int n, int k, vll& memo1, vll& memo2, vll& memo);
lli f1(int n, int k, vll& memo1, vll& memo2, vll& memo);
lli  f2(int n, int k, vll& memo1, vll& memo2, vll& memo);


lli f(int n, int k, vll& memo1, vll& memo2, vll& memo) {
    if (n == 0) {
        return 0;
    }
    if (k < 1) {
        return 0;
    }

    if (memo[n] != - 1) {
        return memo[n];
    }

    auto res = (k - 1) * f1(n - 1, k, memo1, memo2, memo) +
            k * f2(n - 1, k, memo1, memo2, memo);


    memo[n] = mod(res, M);
    return memo[n];
}

lli  f1(int n, int k, vll& memo1, vll& memo2, vll& memo) {
    if (n == 1) {
        return 0;
    }
    if (memo1[n] != -1) {
        return memo1[n];
    }

    memo1[n] = mod(f2(n - 1, k, memo1, memo2, memo), M);
    return memo1[n];
}

lli  f2(int n, int k, vll& memo1, vll& memo2, vll& memo) {
    if (n == 1) {
        return k;
    }

    if (memo2[n] != -1) {
        return memo2[n];
    }

    memo2[n] = (k - 1) * f(n - 1, k, memo1, memo2, memo);
    memo2[n] = mod(memo2[n], M);
    return memo2[n];
}


lli countWays(int n, int k){

    std::vector<lli>  memo {n + 1,  -1};
    std::vector<lli>  memo1 {n + 1,  -1};
    std::vector<lli>  memo2 {n + 1,  -1};

    // code here

    return f(n, k, memo1, memo2, memo);
}
