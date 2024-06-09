# include<cmath>
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

