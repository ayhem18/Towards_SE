// for input and output 
# include <stdio.h> 
# include <stdlib.h>
# include "headers/dataStructures/linear/linked_list.h"

// for the is_prime function
// # include "math_utils.h"
// # include "array_utils.h"


# include <unistd.h>


int process_function() {
    printf("hello world from (pid: %d)\n", (int) getpid()); // this the process id of the current process

    int rc = fork(); 
    
    if (rc < 0) {
        // fork failed; exit
        fprintf(stderr, "fork failed\n");
        exit(1);

    } else if (rc == 0) {
        // child (new process)
        printf("hello, I am child process (pid: %d)\n", (int) getpid());

        for (int i = 0; i < 10; i++) {
            printf("child process wasting CPU time\n");
            sleep(0.3); // sleep for approximately 0.3 seconds 
        }        
    
    } else {
        // the wait call here is used to wait for the child process to finish
        wait(NULL);
 
        // parent process
        printf("hello, I am parent of %d (pid: %d)\n", rc, (int) getpid());
    }

    return 0;
}


int main() {
    return process_function();
}

// int main() {
//     // create a linked list
//     LinkedList* list = create_linked_list();
    
//     add_node(list, 1);
//     add_node(list, 2);
//     add_node(list, 3);
//     print_list(list);
//     free_list(list);
//     printf((list == NULL));

// }
