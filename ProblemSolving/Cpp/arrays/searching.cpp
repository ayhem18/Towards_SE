# include "searching.h"
# include <algorithm>


std::vector <int> commonElements (int a1[], int a2[], int n1, int n2){
    std::vector<int> common{};
    int i1 = 0, i2 = 0;
    while ((i1 < n1) && (i2 < n2)) {
        int * min_array = (a1[i1] <= a2[i2]) ? a1 : a2;
        int min_index = (a1[i1] <= a2[i2]) ? i1: i2;
        int min_size = (a1[i1] <= a2[i2]) ? n1 : n2;

        int * max_array = (a1[i1] > a2[i2]) ? a1 : a2;
        int max_index = (a1[i1] > a2[i2]) ? i1 : i2;
        int max_size = (a1[i1] > a2[i2]) ? n1: n2;

        while ((min_index < min_size) && (min_array[min_index] < max_array[max_index])) {
            min_index ++;
        }

        // there are 3 possible scenarios at this case
        // either min_dex = min_size
        if (min_index == min_size) {
            // this means that we reached the end of the min_array; no more common elements
            return common;
        }

        // if min_array[min_index] == max_array[max_index]
        if (min_array[min_index] == max_array[max_index]) {
            int initial_value = min_array[min_index];
            // to avoid reporting the common elements multiple times
            while((min_index < min_size)
            && (max_index < max_size)
            && (min_array[min_index] == initial_value)
            &&(max_array[max_index] == initial_value)) {
                min_index ++;
                max_index ++;
            }
            common.push_back(min_array[min_index - 1]);
        }
        i1 = (a1[i1] <= a2[i2]) ? min_index : max_index;
        i2 = (min_index == i1) ? max_index: min_index;
    }
    return common;
}


std::vector <int> commonElements (int A[], int B[], int C[], int n1, int n2, int n3) {
    /**
     * https://www.geeksforgeeks.org/find-common-elements-three-sorted-arrays/?ref=roadmap
     */
    // get the common elements between A and B
    std::vector<int> commonAB = commonElements(A, B, n1, n2);
    const int n = static_cast<int>(commonAB.size());
    int commonArray[n];
    for (int i = 0; i < n; i++ ) {
        commonArray[i] = commonAB[i];
    }
    return commonElements(commonArray, C, n, n3);
}



std::vector<int> leaders(int n, int arr[]) {
    // the idea here is to calculate the maximum number starting from the right
    int maxes[n];
    int current_max = arr[n-1];
    for (int i = n - 1; i >= 0; i--) {
        current_max = std::max(current_max, arr[i]);
        maxes[i] = current_max;
    }
    std::vector<int> leaders {};
    for (int i = 0; i < n; i ++) {
        if (arr[i] == maxes[i]) {
            leaders.push_back(arr[i]);
        }
    }
    return leaders;
}


int search_function(int arr[], int low, int high) {
    while (high > low) {
        int mid = static_cast<int> ((low + high) / 2);

        if ((arr[mid] != arr[mid + 1]) && (arr[mid]  != arr[mid - 1])) {
            return arr[mid];
        }

        // at this point it depends on the value of mid
        if (arr[mid] == arr[mid + 1]) {
            if (mid % 2 == 0) {
                low = mid;
            }
            else {
                high = mid;
            }
        }
        else {
            if (mid % 2 == 0) {
                high = mid;
            }
            else {
                low = mid;
            }
        }

    }

    return arr[low];
}

int search(int n, int arr[]) {
    /*
    Solve:
    
    https://www.geeksforgeeks.org/problems/element-appearing-once2552/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card
    */

    if (n == 1) {
        return arr[0];
    }
    
    if (arr[0] != arr[1]) {
        return arr[0];
    }

    if (arr[n - 1] != arr[n - 2]) {
        return arr[n - 1];
    }

    return search_function(arr, 0, n - 1);
}
