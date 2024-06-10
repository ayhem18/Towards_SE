# include<cmath>
# include <algorithm>
int mod(int a , int b) {
    return ((a % b) + b) % b;
}

int numberSequenceQ0(int m, int n, int q0) {
    if (n < 1) {
        return 1;
    }
    int count = 0;
    int lower_bound = 2 * q0;
    int upper_bound = static_cast<int> (m / pow(2, n - 1));
    for (int q1 = lower_bound; q1 <= upper_bound; q1 ++ ){
        count += numberSequenceQ0(m, n - 1, q1);
    }
    return count;
}

int numberSequence(int m, int n) {
    // find the possible q0
    int upper_bound = static_cast<int> (m / pow(2, n - 1));
    int count = 0;
    for (int q0 = 1; q0 <= upper_bound; q0 ++ ){
        count += numberSequenceQ0(m, n - 1, q0);
    }
    return count;
}


int findOnceRec(int arr[], int high, int low) {
    // high - low + 1 must be odd for this solution to work
    if (high == low) {
        return arr[low];
    }

    int mid = (high + low) / 2;

    if (arr[mid] == arr[mid + 1]) {
        if (mod(high - mid, 2)  == 0) {
            return findOnceRec(arr, high, mid);
        }
        return findOnceRec(arr, mid - 1, low);
    }

    if (arr[mid] == arr[mid - 1]) {
        if (mod(mid - low, 2) == 0) {
            return findOnceRec(arr, mid, low);
        }
        return findOnceRec(arr, high, mid + 1);
    }

    // if arr[mid] different from both its successor and predecessor, then we found our element
    return arr[mid];
}

int findOnce(int arr[], int n)
{
// the array is sorted and all elements repeat twice but a single one. I need to find the element that repeats only once
    return findOnceRec(arr, n - 1, 0);
}


int kthElementIndex(int a1[], int a2[], int n, int m, int k) {
    // let's start with few base cases
    if (k == 0) {
        return std::min(a1[0], a2[0]);
    }

    if (k == 1) {
        if (a1[0] == a2[0]) {
            return a1[0];
        }
        if (a1[0] < a2[0]) {
            if (n >= 2){
                return std::min(a1[1], a2[0]);
            }
            return a2[0];
        }
        if (a1[0] > a2[0]) {
            if (m >= 2){
                return std::min(a2[1], a1[0]);
            }
            return a1[0];
        }
    }

    if (k == n + m - 1) {
        return std::max(a1[n - 1], a2[m - 1]);
    }

    // let's consider the case where the final sorted array is simply
    // a concatenation of both arrays
    if (a1[0] >= a2[m - 1]) {
        // so every element in a2 is less than every element in a1
        if (k < m) {
            return a2[k];
        }
        return a1[k - m];
    }

    // let's consider the case where the elements are not merged
    if (a2[0] >= a1[n - 1]) {
        // so every element in a1 is less than every element in a2
        if (k < n) {
            return a1[k];
        }
        return a2[k - n];
    }

    // at this point we know that the final sorted array is obtained by merging and not concatenating the arrays
    int min_size = std::min(n, m);
    int max_size = std::max(n, m);
    int* min_size_array = (n < m) ? a1 : a2;
    int* max_size_array = (n >= m) ? a1 : a2;

    int k2 = ceil(k / 2.0);

    if (k2 >= min_size) {
        int new_min_size = ceil(min_size / 2.0);
        int new_max_size = k - min_size;
        if (max_size_array[new_max_size - 1] >= min_size_array[new_min_size - 1]) {
            return kthElementIndex(min_size_array, max_size_array, min_size, new_max_size, k);
        }
        return kthElementIndex(min_size_array, max_size_array, new_min_size, max_size, k);
    }

    if (min_size_array[k2] <= max_size_array[k2]) {
        return kthElementIndex(min_size_array, max_size_array, min_size, k2, k);
    }

    return kthElementIndex(min_size_array, max_size_array, k2, max_size, k);
}


// this function is the solution for the following problem
// https://www.geeksforgeeks.org/problems/k-th-element-of-two-sorted-array1317/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=bottom_sticky_on_article
int kthElement(int arr1[], int arr2[], int n, int m, int k){
    // for some reason 'k' is not 0-index in the task description
    return kthElementIndex(arr1, arr2, n, m, k - 1);
}





