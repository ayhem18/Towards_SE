#ifndef CPP_HASH_MAP_SET_H
#define CPP_HASH_MAP_SET_H

# include <unordered_map>
# include <vector>
# include <set>

using vi = std::vector<int>;

bool map_subset_map(std::unordered_map<char, vi> m1, std::unordered_map<char, int> m2);

std::vector<int> removeDuplicate(std::vector<int>& arr);


#endif 