# pragma once

# include <stdio.h> // needed for the printf function
# include <stdlib.h> // needed for the NULL definition

typedef struct Node {
    int data;
    struct Node* next;
} Node;

// no need to explore the create_node function to the user...

// Node* create_node(int data);


typedef struct LinkedList {
    Node* head;
} LinkedList;


LinkedList* create_linked_list();

void add_node(LinkedList* list, int data);

void print_list(LinkedList* list);

void free_list(LinkedList* list);
