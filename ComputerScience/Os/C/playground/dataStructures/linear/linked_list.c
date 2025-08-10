# include "../../headers/dataStructures/linear/linked_list.h"

Node* create_node(int data) {
    Node* node = malloc(sizeof(Node));
    node -> data = data;
    node -> next = NULL;
    return node;
}

LinkedList* create_linked_list() {
    LinkedList* list = malloc(sizeof(LinkedList));
    list -> head = NULL;
    return list;
}


void add_node(LinkedList* list, int data) {
    if (list -> head == NULL) {
        list -> head = create_node(data);
        return;
    }

    // at this point we know there is at least one node in the list

    Node* traverse_node = list -> head;
    while (traverse_node -> next != NULL) {
        traverse_node = traverse_node -> next;
    }

    // at this point we reached the last node in the list
    // create a new node and set it as the next node of the last node 
    traverse_node -> next = create_node(data);

}


void print_list(LinkedList* list) {
    Node* traverse_node = list -> head;

    if (traverse_node == NULL) {
        printf("List is empty\n");
        return;
    }

    printf("%d", traverse_node -> data);
    traverse_node = traverse_node -> next;

    // this way avoiding to have the following display : number ->  for a list with only one node
    while (traverse_node != NULL) {
        printf("-> %d", traverse_node -> data);
        traverse_node = traverse_node -> next;
    }
    printf("\n");
}

void _free_empty_list(LinkedList* list) {
    free(list);
    list = NULL;
}


void free_list(LinkedList* list) {
    
    if (list -> head == NULL) {
        // free the empty linked list
        _free_empty_list(list);
        return;
    }

    Node* traverse_node = list -> head;
    while (traverse_node != NULL) {
        Node* next_node = traverse_node -> next;
        free(traverse_node);
        traverse_node = next_node;
    }

    // free the empty linked-list   
    _free_empty_list(list);
}


