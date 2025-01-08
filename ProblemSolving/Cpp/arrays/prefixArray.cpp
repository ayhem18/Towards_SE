/*
This file contains my solutions to problems that can be solved using the prefixArray idea
*/

# include <set> // for the set datastructure
# include <map> // for the map datastructure
# include "../utils.h" // my file with the utils functions



// this problem does not exactly use the PrefixArray, but it is mainly about understanding how to use sums !! (close enough, I guess)
void update(int a[], int n, int updates[], int k) {
    /**
     * https://www.geeksforgeeks.org/problems/adding-ones3628/1
     */
     for (int i=0; i <k; i++) {
         int index = updates[i] - 1;
         a[index] ++;
     }

     int total = 0;
     for(int i=0;i<n;i++){
         total += a[i];
         a[i] = total;
     }
}

// this problem does not exactly use the PrefixArray, but it is mainly about understanding how to use sums !! (close enough, I guess)
int equilibriumPoint(long long arr[], int n) {
    if (n == 1) {
        return 1;
    }

    long long total = 0;
    for (int i = 0; i < n; i ++) {
        total += arr[i];
    }
    long long sum = 0;
    for (int i = 0; i < n; i ++) {
        // at this point sum contains the sum of elements from [0, i-1]
        long long right_sum = total - sum - arr[i];
        if (right_sum == sum) {
            return i + 1;
        }
        sum += arr[i];
    }
    return -1;
}


bool subArrayExists(int arr[], int n){
    /**
     * https://www.geeksforgeeks.org/problems/subarray-with-0-sum-1587115621/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
     */

    // let's create the preFixSum array
    int total = 0;
    int prefixSum [n];
    for (int i=0; i < n; i ++) {
        total += arr[i];
        prefixSum[i] = total;
    }

    // first check if any of the sub-arrays [0, i] sub to zero

    for (int i = 0; i < n; i ++) {
        if (prefixSum[i] == 0) {
            return true;
        }
    }

    // if all values in the prefixSum array are distinct
    // then there is no subarray that sums up to 0
    std::set<int> distinct_sums;
    for (int i = 0; i < n; i++) {
        distinct_sums.insert(prefixSum[i]);
    }

    return distinct_sums.size() != n;
}



int longSubarrWthSumDivByK(int arr[], int n, int k){
    /*
    Solve: https://www.geeksforgeeks.org/problems/longest-subarray-with-sum-divisible-by-k1259/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
    basically this function finds the longest subarray with a sum divisible by "K"

    1. first step consider sub arrays from [0, i], set the max_length to i + 1, for any subarray [0, i] satisfying the condition
    2. for each reminder of 0, 1, 2.. k - 1, save the indices "i"s such that [0, i] % K == j
    3. then basically the largest subarray divisible by k would start at i1 and ends at i2 where [0, i1] and [0, i2] have the same reminder with respect to "k"
    */

    int prefixSum[n];
    int total = 0;
    for (int i = 0; i < n; i ++) {
        total += arr[i];
        prefixSum[i] = mod(total, k);
    }

    int max_len = -1;
    // first let's find any prefix subarray that are divisible by 'K'
    for (int i = 0; i < n;i ++) {
        if (prefixSum[i] == 0) {
            max_len = i + 1;
        }
    }

    if (max_len == n) {
        return n;
    }

    std::map<int, std::pair<int,int>> mods_indices;

    for (int i = 0;i < n; i++) {
        if (mods_indices.contains(prefixSum[i])) { // make sure to set the C++ standard to at least 20 for this function to work...
            mods_indices[prefixSum[i]].second = i;
        }
        else {
            mods_indices[prefixSum[i]] = std::pair(i, -1);
        }
    }

    // iterate through the map
    for (int i = 0; i < n; i++) {
        auto p = mods_indices[prefixSum[i]];
        if (p.second != -1) {
            max_len = std::max(max_len, p.second - p.first);
        }
    }

    return max_len;
}



std::vector<int> subarraySum(std::vector<int>& arr, int n, long long s) {
    /*
    Solve: https://www.geeksforgeeks.org/problems/subarray-with-given-sum-1587115621/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
    */

    for (int i = 0; i < n; i++) {
        if (s == 0 and arr[i] == 0) {
            return {i + 1, i + 1};
        }
    }

    if (s == 0) {
        return {-1};
    }

    // compute the prefix array
    std::vector<int> ps (n, 0);
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
        ps[i] = total;
    }

    // iterate through the prefix array
    for (int i = 0; i < n; i++) {
        if (ps[i] == s) {
            return {1, i + 1};
        }
    }

    std::vector<int> psi (n, 0);
    for (int i = 0; i < n; i++) {
        psi[i] = -ps[n - 1 - i];
    }


    // the idea now is to find indices i1, i2 such that ps[i1] + psi[i2] sum up to 's'
    int i1 = 0;
    int i2 = n - 1;

    while (i1 < n and i2 >= 0) {
        if (ps[i1] + psi[i2] > s) {
            i2 = i2 - 1;
        }

        else if (ps[i1] + psi[i2] < s) {
            i1 += 1;
        }

        else {
            int real_index = n - 1 - i2;
            if (real_index <= i1) {
                return {real_index + 2, i1 + 1};
            }
            return {i1 + 2, real_index + 1};
        }
    }

    return {-1, -1};
}
