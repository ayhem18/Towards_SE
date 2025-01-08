# include <set>
# include "prefixSum.h"
# include "../utils.h"
# include <map>
# include <utility>

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


// int longSubarrWthSumDivByK(int arr[], int n, int k){
//     int prefixSum[n];
//     int total = 0;
//     for (int i = 0; i < n; i ++) {
//         total += arr[i];
//         prefixSum[i] = mod(total, k);
//     }

//     int max_len = -1;
//     // first let's find any prefix subarray that are divisible by 'K'
//     for (int i = 0; i < n;i ++) {
//         if (prefixSum[i] == 0) {
//             max_len = i + 1;
//         }
//     }

//     if (max_len == n) {
//         return n;
//     }

//     std::map<int, std::pair<int,int>> mods_indices;

//     for (int i = 0;i < n; i++) {
//         if (mods_indices.contains(prefixSum[i])) {
//             mods_indices[prefixSum[i]].second = i;
//         }
//         else {
//             mods_indices[prefixSum[i]] = std::pair(i, -1);
//         }
//     }

//     // iterate through the map
//     for (int i = 0; i < n; i++) {
//         auto p = mods_indices[prefixSum[i]];
//         if (p.second != -1) {
//             max_len = std::max(max_len, p.second - p.first);
//         }
//     }

//     return max_len;
// }


