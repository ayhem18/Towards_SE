#ifndef LEARNC___BASICS_H
#define LEARNC___BASICS_H

# include <vector>

std::vector<int> bfsOfGraph(int V,
                            std::vector<int> adj[]);

std::vector<int> dfsOfGraph(int V, std::vector<int> adj[]);

int maxWeightCell(int n, std::vector<int> edges);

#endif //LEARNC___BASICS_H
