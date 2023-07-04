def __binary_search(array: list, x, low, high):
    while low <= high:

        mid = low + (high - low) // 2

        if array[mid] == x:
            return mid

        elif array[mid] < x:
            low = mid + 1

        else:
            high = mid - 1

    return -1


def binary_search(array, x):
    return __binary_search(array, x, 0, len(array))




