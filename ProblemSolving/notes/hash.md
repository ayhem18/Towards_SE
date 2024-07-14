# Hashing: The main ideas

The low-level implementation details of the has data structure are indeed fascinating. Yet, they are not of substantial importance for solving algorithmic problems. The main points: 

* memberships in O(1) time (on average): need to know $val \in array$ in O(1) time ? represent the array as a ***dictionary***
* having key-value pairs and finding key(val) in O(1); save them in a ***dictionary*** 
    * frequency of elements in a certain structure: array / string.

# Hashing Combinations
Hashing by itself is of limited usefulness Nevertheless, combined with other data structures, it can be a powerful tool. 

## Hash + Queue
The most efficient suggested solution for [this problem](https://www.geeksforgeeks.org/given-a-string-find-its-first-non-repeating-character/#efficient-approach-1-using-hash-map-on-time-and-o1-auxiliary-space) combines the QUEUE and the HASH ds;  [My solution](..\Python\hashing\gfg1.py)

