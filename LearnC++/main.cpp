# include <vector>
# include <string>
#include <bits/stdc++.h>

void print_vector(const std::vector<int>& int_vec);
void print_vector(const std::vector<double>& double_vec);
std::string getStringInput(const std::string& input_prompt);

int getIntegerInput(const std::string& prompt_text);
bool containsDuplicate(std::vector<int>& nums);

void insertion_sort_insert_min(std::vector<int>& vec);
void insertion_sort_insert_max(std::vector<int>& vec);
void sort_STL(std::vector<int>& vec){
    std::sort(vec.begin(), vec.end());
}
std::vector<int> merge_sorted_arrays(std::vector<int>& left, std::vector<int>& right);
std::vector<int> merge_sort(std::vector<int>& vec);


struct ListNode {
    int val;
    ListNode *next;
};

ListNode* insert_element(ListNode * head, int value);
void print_linked_list(ListNode* head);
bool hasCycle(ListNode *head);


int main() {
//    std::vector<int> v1 {4, 2, -4, 10, 23, 0, -5};
//    std::vector<int> v2 {1, 2, 5, 3};
//    std::vector<int> v1_sorted = merge_sort(v1);
//    std::vector<int> v2_sorted = merge_sort(v2);
//    print_vector(v1_sorted);
//    print_vector(v2_sorted);

    // setting the initial head
    ListNode* head = new ListNode();
    head -> val = 1;
    head -> next = nullptr;

    for (int i = 2; i <= 4; i ++) {
        head = insert_element(head, i);
    }
    print_linked_list(head);

    std::cout << std:: boolalpha << hasCycle(head) << "\n";

    // let's create a cyclic linked list
    ListNode* n1 = new ListNode();
    n1->val = 1;

    ListNode* n2 = new ListNode();
    n2->val = 2;

    ListNode* n3 = new ListNode();
    n3->val = 3;

    n1 -> next = n2;
    n2 -> next = n3;
    n3 -> next = n2;

    std::cout << std::boolalpha << hasCycle(n1) << "\n";
}

