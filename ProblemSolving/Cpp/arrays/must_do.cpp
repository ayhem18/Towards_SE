/**
* This script contains the solutions for the problems listed in the
*/

# include<vector>
std::vector<int> subarraySum(std::vector<int>& arr, int n, long long s) {
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
    int cum_sum = 0;
    for (int i = 0; i < n; i++) {
        cum_sum += arr[i];
        ps[i] = cum_sum;
    }

    // iterate through the cum_sum array
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


