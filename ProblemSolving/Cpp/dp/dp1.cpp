# include "../utils.h"
# include <cmath>
# include <vector>




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

lli countWays(int n, int k) {
    if (k <= 1) {
        if (n > 2) {
            return 0;
        }
        return 1;
    }
    // we know that k >= 2
//    lli dp[n + 1][3];
//
//    dp[0][0] = 0;
//    dp[0][1] = 0;
//    dp[0][2] = 0;
//
//    dp[1][0] = 0;
//    dp[1][1] = k;
//    dp[1][2] = k;


    lli n1Prev = 0, n2Prev = k, n3Prev = k;
    lli n1 = 0, n2 = k , n3 = k;

    for (int i = 2; i <= n; i++) {
        n1 = n2Prev;
        n2 = mod((k - 1) * n3Prev, M);
        n3 = mod((k - 1) * n1Prev + k * n2Prev, M);
        n1Prev = n1;
        n2Prev = n2;
        n3Prev = n3;
    }
//    for (int i = 2; i <= n; i++) {
//        dp[i][0] = dp[i - 1][1];
//        dp[i][1] = mod((k - 1)  * dp[i - 1][2], M);
//        dp[i][2] = mod((k - 1) * dp[i - 1][0] + k * dp[i - 1][1], M);
//    }
    return n3;
//    return dp[n][2];
}

lli countWaysDP(int n, int k) {
    if (k <= 1) {
        if (n > 2) {
            return 0;
        }
        return 1;
    }
    // we know that k >= 2
    lli dp[n + 1][3];

    dp[0][0] = 0;
    dp[0][1] = 0;
    dp[0][2] = 0;

    dp[1][0] = 0;
    dp[1][1] = k;
    dp[1][2] = k;


    for (int i = 2; i <= n; i++) {
        dp[i][0] = dp[i - 1][1];
        dp[i][1] = mod((k - 1)  * dp[i - 1][2], M);
        dp[i][2] = mod((k - 1) * dp[i - 1][0] + k * dp[i - 1][1], M);
    }
    return dp[n][2];

}
