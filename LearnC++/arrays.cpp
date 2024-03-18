#include <vector>
#include <bits/stdc++.h>
#include <algorithm>

using namespace std;
bool containsDuplicate(vector<int>& nums) {
    // first let's get the size of the array
    int n{static_cast<int>(nums.size())};

    // sort the array
    sort(nums.begin(), nums.end());

    int last_num{nums.at(0)};
    for (int i = 1; i < n; i ++ ){
        if (last_num == nums[i]) {
            return true;
        }
        last_num = nums[i];
    }
    return false;
}

void insertion_sort_insert_min(vector<int>& vec) {
    // assuming we have the array[:i] sorted
    // then it suffices to insert a[i + 1] in the correct position to have a[: i + 1]
    // inserting can simply take place by moving a[i + 1] down until we find an element less or equal than a[i + 1]
    int vec_length {static_cast<int> (vec.size())};
    for (int i = 1; i < vec_length; i++) {
        // first save the current value
        int key{vec[i]};
        int j = i - 1;
        while (j >= 0 & vec[j] > key) {
            // the element vec[j] is larger than key, then vec[j] should be pushed forward
            vec[j + 1] = vec[j];
            j--;
        }
        vec[j + 1] = key;
    }
}


void insertion_sort_insert_max(vector<int>& vec) {
    // let's use a very similar version of insertion sort
    // but one that pushes maximum forward
    int n {static_cast<int> (vec.size())};
    for (int i = n - 2; i >= 0; i--) {
        int key = vec[i];
        int j = i + 1;
        while (j < n & key > vec[j]) {
            vec[j - 1] = vec[j];
            j++;
        }
        vec[j - 1] = key;
    }
}


std::vector<int> slice_vector(const std::vector<int>& vec,
                              int start_index,
                              int end_index);


std::vector<int> merge_sorted_arrays(std::vector<int>& left, std::vector<int>& right) {
    int n1{static_cast<int>(left.size())};
    int n2{static_cast<int>(right.size())};

    // does the code handle the degenerate cases ?
    vector<int> result = {};
    int i1 = 0;
    int i2 = 0;
    while (i1 < n1 & i2 < n2) {
        if (left[i1] <= right[i2]) {
            result.push_back(left[i1]);
            i1 ++;
        }
        else{
            result.push_back(right[i2]);
            i2 ++;
        }
    }

    if (i1 == n1) {
        result.insert(result.end(), right.begin() + i2, right.end());
    }
    else{
        result.insert(result.end(), left.begin() + i1, left.end());
    }
    return result;
}

vector<int> merge_sort(vector<int>& vec) {
    // the first step is the base case
    int n{static_cast<int> (vec.size())};
    if (n == 1)
        return vec;
    if (n == 2)
        return {min(vec[0], vec[1]), max(vec[0], vec[1])};

    // at this point we know the array has more than 2 elements
    // split the array in 2
    vector<int> left = slice_vector(vec, 0, n / 2);
    vector<int> right = slice_vector(vec, n / 2 + 1, n - 1);

    // sort the left side
    left = merge_sort(left);
    // sort the right side
    right = merge_sort(right);

    // merge both arrays
    return merge_sorted_arrays(left, right);
}


