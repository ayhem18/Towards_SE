// this file contains my attempts to solve the graph problems suggested by the NeetCode 150 problems (the Graph section)

# include <vector>
# include <unordered_map>
/**
 * https://leetcode.com/problems/number-of-islands/
 */

int numIslands(std::vector<std::vector<char>>& grid) {
    // build a graph representation of the island: each piece of land (square) represents a vertex
    // an island is a connected component
    int counter = 0;
    int n1 = static_cast<int>(grid.size()), n2 = static_cast<int>(grid[0].size());

    // create a map between the coordinates and the counter
//    std::unordered_map<std::pair<int, int>, int> coords_counter_map {{0:1}};
//
//    for (int i = 0; i < n1; i++) {
//        for (int j = 0; j < n2; j++) {
//            if (grid[i][j] == '1') {
//
//            }
//        }
//    }
}
