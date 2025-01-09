/*
This file contains my solutions for gfg problems that can be solved mainly using a hashmap or a set
*/ 

# include "hash_map_set.h"

bool map_subset_map(std::unordered_map<char, vi> m1, std::unordered_map<char, int> m2) {

    // check if m2 is a subset of m1
    auto it = m2.begin();
    while (it != m2.end()) {
        char key = it -> first;
        // check if the key is in m1

        auto m1_key = m1.find(key);
        if (m1_key == m1.end()) {
            return false;
        }

        // check the occurrence
        if ((m1_key -> second).size() < it -> second){
            return false;
        }
        it ++;
    }
    return true;
}


// the main goal of solving this problem is to refresh the C++ syntax in my head

std::vector<int> removeDuplicate(std::vector<int>& arr) {
    // the idea is very 
    std::set arr_set = std::set<int>();

    vi new_arr = vi();

    for (const int v : arr) {
        if (arr_set.find(v) == arr_set.end()) {
        // if (! arr_set.contains(v) ) {
            new_arr.push_back(v);
            arr_set.insert(v);
        }
    }
    return new_arr;
}


// std::string smallestWindow (std::string& s, std::string& p) {

//     // consider the case where p is of length 1 independently
//     if (p.size() == 1) {
//         if (s.find(p) != std::string::npos) {
//             return p;
//         }
//         return "-1";
//     }


//     // let's build p as a dictionary
//     std::unordered_map<char, int> p_map{};
//     for (char c: p) {
//         if (p_map.find(c) == p_map.end()) {
//             p_map[c] = 1;
//         } else {
//             p_map[c] += 1;
//         }
//     }

//     int best_start = -1, best_end = static_cast<int>(s.size());

//     // let's first find a good start
//     int start = 0;
//     while (p_map.find(s[start]) == p_map.end()) {
//         start++;
//     }
//     // at this point of the program we know that p has at least two elements
//     // hence end should be at least start + 1

//     int end = start + 1;

//     // at this point we know that s[start] is common with 'p'
//     std::unordered_map<char, vi> segment_map = {{s[start], {start}}};

//     int n = static_cast<int> (s.size());

//     while (end < n) {
//         // check if s[end] is in the p_map
//         if (p_map.find(s[end]) != p_map.end()) {
//             // append the value of 'end' to the vector associated with s[end]
//             if (segment_map.find(s[end]) == segment_map.end()) {
//                 segment_map[s[end]] = {end};
//             } else {
//                 segment_map[s[end]].push_back(end);
//             }
//             // check if the segment contains 'p'
//             bool segment_contains_p = map_subset_map(segment_map, p_map);

//             if (segment_contains_p) {
//                 if (end - start < best_end - best_start) {
//                     // update the best segment
//                     best_start = start;
//                     best_end = end;
//                 }
//                 // time to update the 'start' variable:
//                 // first remove it from the segment
//                 // choose start as the smallest value in the current segment
//                 auto it = segment_map.begin();

//                 int index_to_remove = start;
//                 char char_to_remove = s[start];

//                 while (it != segment_map.end()) {
//                     int size = static_cast<int>((it->second).size());
//                     int needed_size = p_map[it->first];

//                     if (size == needed_size) {
//                         it ++ ;
//                         continue;
//                     }

//                     int new_index = (it->second)[size - needed_size - 1];

//                     if (new_index > index_to_remove) {
//                         index_to_remove = std::max(index_to_remove, new_index);
//                         char_to_remove = it->first;
//                     }
//                     it ++ ;
//                 }

//                 int needed_size = p_map[char_to_remove], size = segment_map[char_to_remove].size();
//                 auto b = segment_map[char_to_remove].begin(), e = b + size - needed_size;
//                 segment_map[char_to_remove].erase(b, e);

//                 int new_start = end;
//                 it = segment_map.begin();
//                 // find the new start
//                 while (it != segment_map.end()) {
//                     new_start = std::min((it->second)[0], new_start);
//                     it ++;
//                 }

//                 start = new_start;
//                 std::string r = "";
//             }

//         }

//         end++;
//     }

//     bool segment_contains_p = map_subset_map(segment_map, p_map);
//     if (segment_contains_p) {
//         if (end - start < best_end - best_start) {
//             // update the best segment
//             best_start = start;
//             best_end = end;
//         }
//     }
//     // make sure to consider the case where a match is not found
//     if (best_start == -1) {
//         return "-1";
//     }

//     return s.substr(best_start, best_end - best_start + 1);
// }