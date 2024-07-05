# include "../utils.h"
# include <cmath>
# include <vector>
# include <string>
# include <numeric>
#include <limits>
#include <algorithm>

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
lli _countWays(int n, int k) {
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
lli _countWaysDP(int n, int k) {
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



/**
* https://www.geeksforgeeks.org/problems/number-of-coins1824/1?page=1&category=Dynamic%20Programming&status=unsolved&sortBy=submissions
*/


int _minCoins(std::vector<int> & coins, int n, int sum, std::vector<std::vector<int>>& memo) {
    if (sum <= 0) {
        return -1;
    }

    if (memo[sum][n] != 0){
        return memo[sum][n];
    }

    if (n == 0) {
        if (mod(sum, coins[0]) == 0) {
            memo[sum][0] = sum / coins[0];
        }
        else{
            memo[sum][0] = -1;
        }
        return memo[sum][0];
    }

    int max_num_coins = sum / coins[n];

    int res = std::numeric_limits<int>::max();
    bool modified = false;
    for (int i = 0; i <= max_num_coins; i++) {
        if (sum == i * coins[n]) {
            res = std::min(res, i);
            modified = true;
            continue;
        }

        int temp_res = _minCoins(coins, n - 1, sum - coins[n] * i, memo);
        if (temp_res != -1) {
            res = std::min(res, temp_res + i);
            modified = true;
        }
    }

    // if at this point the value
    if (! modified) {
        res = -1;
    }
    memo[sum][n] = res;
    return res;
}

int minCoins(std::vector<int> &coins, int n, int sum){
    // prepare the dp memory
    std::vector<std::vector<int>> memo(sum + 1);
    for(int i = 0; i < sum + 1; i++) {
        memo[i] = std::vector<int>(n, 0);
    }
    return _minCoins(coins, n - 1, sum, memo);
}


/**
 * https://www.geeksforgeeks.org/problems/longest-common-subsequence-1587115620/1?page=1&category=Dynamic%20Programming&status=unsolved&sortBy=submissions
 */
int lcs(int n, int m, std::string& str1, std::string& str2) {
    // this is somewhat a known problem
    std::vector<std::vector<int>> dp(n + 1);
    for (int i = 0; i <= n; i++) {
        dp[i] = std::vector<int>(m + 1, 0);
    }

    // fill the grid
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            int res = std::max(std::max(dp[i - 1][j], dp[i][j-1]), dp[i - 1][j - 1] + int(str1[i - 1] == str2[j - 1]));
            dp[i][j] = res;
        }
    }

    return dp[n][m];
}


/**
 *
 */
int countWaysDp(int n, vi& memo) {
    int M_int = static_cast<int>(pow(10, 9) + 7);

    if (n <= 0){
        return 1;
    }
    if (n == 1) {
        return 1;
    }

    if (memo[n] != 0) {
        return memo[n];
    }

    int p1 = countWaysDp(n - 2, memo);
    int p2 = countWaysDp(n - 1, memo);

    p1 = mod(p1, M_int);
    p2 = mod(p2, M_int);

    memo[n] = mod(p1 + p2, M_int);
    return memo[n];
}

int countWays(int n) {
    vi memo(n + 1, 0);
    if (n <= 0){
        return 1;
    }
    if (n == 1) {
        return 1;
    }

    memo[0] = 1;
    memo[1] = 1;
    return countWaysDp(n, memo);
}



lli minTimeDp(int arr[], int n, int index, int k, std::vector<vll>& memo) {
    // let's take some base cases
    if (index == 0) {
        return 0;
    }
    if (index == 1) {
        return arr[n - 1];
    }

    if (k == 1) {
        return std::accumulate(arr + n - index, arr + n, 0);
    }

    if (memo[index][k] != 0) {
        return memo[index][k];
    }

    lli first_painter_time = 0;
    lli final_res = std::numeric_limits<lli>::max();

    for (int i = n - index; i < n; i++) {
        first_painter_time += arr[i];
        lli temp_res = minTimeDp(arr, n, n - 1 - i, k - 1, memo);
        lli i_res = std::max(first_painter_time, temp_res);
        final_res = std::min(final_res, i_res);
        if (temp_res <= first_painter_time) {
            break;
        }
    }
    memo[index][k] = final_res;
    return final_res;
}

// the current implementation exceeds time limit
lli minTime(int arr[], int n, int k){
    // prepare the memo
    std::vector<vll> memo;
    for (int i = 0; i < n + 1; i++) {
        memo.push_back(std::vector<lli>(k + 1, 0));
    }
    return minTimeDp(arr, n, n, k, memo);
}


/**
https://www.geeksforgeeks.org/problems/get-minimum-squares0538/1?page=1&difficulty=Medium&status=unsolved&sortBy=submissions
*/
int minSquaresDp(int n, vi& memo) {
    // first check if n is a perfect square
    int n_sqrt = static_cast<int>(sqrt(n));
    if (n == n_sqrt * n_sqrt) {
        return 1;
    }

    if (memo[n] != -1) {
        return memo[n];
    }

    int res = std::numeric_limits<int>::max();

    for (int i = n_sqrt; i >= 1; i --) {
        res = std::min(res,  1 + minSquaresDp(n - i * i, memo));
    }
    memo[n] = res;
    return res;
}

int MinSquares(int n){
    // create the memo
    vi memo(n + 1, -1);
    return minSquaresDp(n, memo);
}

/**
* https://www.geeksforgeeks.org/problems/shortest-common-supersequence0322/1?page=1&difficulty=Medium&status=unsolved&sortBy=submissions
*/
// this problem builds on the longest common subsequence problem

std::pair<vi, vi> lcs(std::string& str1, std::string& str2) {
    int n = static_cast<int> (str1.size()), m = static_cast<int> (str2.size());
    // this is somewhat a known problem
    std::vector<std::vector<int>> dp(n + 1);
    for (int i = 0; i <= n; i++) {
        dp[i] = std::vector<int>(m + 1, 0);
    }

    // fill the grid
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            int res = std::max(std::max(dp[i - 1][j], dp[i][j-1]), dp[i - 1][j - 1] + int(str1[i - 1] == str2[j - 1]));
            dp[i][j] = res;
        }
    }

    // we need to backtrack, and find the indices of the characters belong to the longest subsequence in each string
    vi indices1 {};
    vi indices2 {};

    int i = n, j = m;
    while (i > 0 && j > 0) {
        if (str1[i - 1] == str2[j - 1] && dp[i][j] == dp[i - 1][j - 1] + 1) {
            indices1.push_back(i);
            indices2.push_back(j);
            j = j - 1;
            i = i - 1;
        }
        else {
            // find the minimum
            std::vector<vi> pos {{i - 1, j - 1}, {i, j - 1}, {i - 1, j}};
            auto res = std::max_element(pos.begin(), pos.end(),
                                       [dp] (vi& p1, vi& p2) {return dp[p1[0]][p1[1]] < dp[p2[0]][p2[1]];});
            i = (*res)[0];
            j = (*res)[1];
        }
    }

    return {indices1, indices2};
}



int shortestCommonSupersequence(std::string& x, std::string& y, int m, int n){
    // first the set of indices
    auto res = lcs(x, y);
    vi indices1 = res.first, indices2 = res.second;

    int len = static_cast<int>(indices1.size());

    if (len <= 1) {
        return m + n - len;
    }

    int final_res = len + (m - indices1[0] - 1) + (n - indices2[0] - 1);
    for (int p = 0; p < len - 1; p++) {
        int str1_chars = (indices1[p] - indices1[p + 1] - 1);
        int str2_chars = (indices2[p] - indices2[p + 1] - 1);
        final_res += (str1_chars + str2_chars);
    }

    final_res += (indices1[len - 1]) + (indices2[len - 1]);
    return final_res;
}
