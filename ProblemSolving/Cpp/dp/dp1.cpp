# include "../utils.h"
# include <cmath>
# include <vector>
# include <string>



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


#include <limits>
#include <unordered_map>

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


/**
 *https://www.geeksforgeeks.org/problems/smallest-window-in-a-string-containing-all-the-characters-of-another-string-1587115621/1?page=2&category=Dynamic%20Programming&status=unsolved&sortBy=submissions
 */

bool map_subset_map(std::unordered_map<char, vi> m1, std::unordered_map<char, int> m2) {
    // check if m2 is a subset of m1
    auto it = m2.begin();
    while (it != m2.end()) {
        char key = it -> first;
        // check if the key is in m1

        auto m1_key = m1.find(key);
        if (m1_key == m1.end()) {
            return false;
        }

        // check the occurrence
        if ((m1_key -> second).size() < it -> second){
            return false;
        }
        it ++;
    }
    return true;
}

# include <unordered_map>
std::string smallestWindow (std::string& s, std::string& p) {

    // consider the case where p is of length 1 independently
    if (p.size() == 1) {
        if (s.find(p) != std::string::npos) {
            return p;
        }
        return "-1";
    }


    // let's build p as a dictionary
    std::unordered_map<char, int> p_map{};
    for (char c: p) {
        if (p_map.find(c) == p_map.end()) {
            p_map[c] = 1;
        } else {
            p_map[c] += 1;
        }
    }

    int best_start = -1, best_end = static_cast<int>(s.size());

    // let's first find a good start
    int start = 0;
    while (p_map.find(s[start]) == p_map.end()) {
        start++;
    }
    // at this point of the program we know that p has at least two elements
    // hence end should be at least start + 1

    int end = start + 1;

    // at this point we know that s[start] is common with 'p'
    std::unordered_map<char, vi> segment_map = {{s[start], {start}}};

    int n = static_cast<int> (s.size());

    while (end < n) {
        // check if s[end] is in the p_map
        if (p_map.find(s[end]) != p_map.end()) {
            // append the value of 'end' to the vector associated with s[end]
            if (segment_map.find(s[end]) == segment_map.end()) {
                segment_map[s[end]] = {end};
            } else {
                segment_map[s[end]].push_back(end);
            }
            // check if the segment contains 'p'
            bool segment_contains_p = map_subset_map(segment_map, p_map);

            if (segment_contains_p) {
                if (end - start < best_end - best_start) {
                    // update the best segment
                    best_start = start;
                    best_end = end;
                }
                // time to update the 'start' variable:
                // first remove it from the segment
                // choose start as the smallest value in the current segment
                auto it = segment_map.begin();

                int index_to_remove = start;
                char char_to_remove = s[start];

                while (it != segment_map.end()) {
                    int size = static_cast<int>((it->second).size());
                    int needed_size = p_map[it->first];

                    if (size == needed_size) {
                        it ++ ;
                        continue;
                    }

                    int new_index = (it->second)[size - needed_size - 1];

                    if (new_index > index_to_remove) {
                        index_to_remove = std::max(index_to_remove, new_index);
                        char_to_remove = it->first;
                    }
                    it ++ ;
                }

                int needed_size = p_map[char_to_remove], size = segment_map[char_to_remove].size();
                auto b = segment_map[char_to_remove].begin(), e = b + size - needed_size;
                segment_map[char_to_remove].erase(b, e);

                int new_start = end;
                it = segment_map.begin();
                // find the new start
                while (it != segment_map.end()) {
                    new_start = std::min((it->second)[0], new_start);
                    it ++;
                }

                start = new_start;
                std::string r = "";
            }

        }

        end++;
    }

    bool segment_contains_p = map_subset_map(segment_map, p_map);
    if (segment_contains_p) {
        if (end - start < best_end - best_start) {
            // update the best segment
            best_start = start;
            best_end = end;
        }
    }
        // make sure to consider the case where a match is not found
    if (best_start == -1) {
        return "-1";
    }

    return s.substr(best_start, best_end - best_start + 1);
}

