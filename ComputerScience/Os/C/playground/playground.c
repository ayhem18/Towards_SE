void array_playground() {
    int arr[] = {1, 2, 3, 4, 5};
    // how to compute the size of an array... 
    int length = ARRAY_LENGTH(arr);
    for (int i = 0; i < length; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);
    }
    printf("\n");

}

// int int_playground(char* argv[]) {
    
//     if (array_length(argv) != 2) {
//         printf("Usage: %s <number>\n", argv[0]);
//         return 0;
//     }

//     int number = atoi(argv[1]);
//     bool is_prim_number = is_prime(number);
//     printf("Is %d prime? %s\n", number, is_prim_number ? "Yes" : "No");
//     return 0;

// }



int main(int argc, char* argv[]) {
    // arrays when passed to a function are passed as function losing size information
    // that's why argc is passed with the function call
    array_playground();
}
    