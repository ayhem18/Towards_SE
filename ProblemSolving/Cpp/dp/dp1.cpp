# include "../utils.h"
# include <cmath>
# include <vector>
# include <utility>
# include <algorithm>

/**
 * these functions below are written to solve:
 * https://www.geeksforgeeks.org/program-for-nth-fibonacci-number/
 */
long long int _topDown(int n, int a[]) {
    int M = static_cast<int> (pow(10, 9) + 7);
    if (a[n] != -1) {
        return mod(a[n], M);
    }

    // make sure to save the value in the value storage
    a[n] = (mod(_topDown(n - 1, a), M) + mod(_topDown(n - 2, a), M));
    a[n] = mod(a[n], M);
    return a[n];
}

long long int topDown(int n) {
    int a[n + 1];
    for (int i = 0; i < n + 1; i++) {
        a[i] = -1;
    }
    a[0] = 0;
    a[1] = 1;
    return _topDown(n, a) ;
}



long long int bottomUp(int n) {
    int arr[n+1];
    arr[0]=0;
    arr[1]=1;
    int M = static_cast<int> (pow(10, 9) + 7);
    for (int i = 2; i < n + 1; i++) {
        arr[i] = mod(arr[i - 1], M) + mod(arr[i - 2], M);
    }
    return mod(arr[n], M);
}

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
