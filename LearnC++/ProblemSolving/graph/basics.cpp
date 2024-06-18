# include <vector>
# include <queue>
# include <map>

std::vector<int> bfsOfGraph(int V,
                            std::vector<int> adj[]) {
    // the graph is expressed as an adjacency list
    // where V is the number of vertices
    // and adj is an array of std::vector<int>

    std::map<int, bool> visited = {};
    // set all the values to false
    for (int i = 0; i < V;i++) {
        visited[i] = false;
    }

    std::vector<int> res {};
    std::queue<int> nbh {};
    nbh.push(0);
    visited[0] = true;
    while (!nbh.empty()){
        int current_node = nbh.front();
        // go through the neighbors
        for (int n : adj[current_node]) {
            if (!visited[n]) {
                nbh.push(n);
                visited[n] = true;
            }
        }

        res.push_back(current_node);
        // make sure to pop the current node
        nbh.pop();
    }
    return res;
}


void dfsGraph(int v, std::vector<int> adj[], std::vector<int>& visited_nodes, std::map<int, bool>& visited_map) {
    for (int n: adj[v]) {
        if (!visited_map[n]) {
            visited_map[n] = true;
            visited_nodes.push_back(n);
            dfsGraph(n, adj, visited_nodes, visited_map);
        }
    }
}

// can't do bfs without dfs baby !!
std::vector<int> dfsOfGraph(int V, std::vector<int> adj[]) {
    std::map<int, bool> visited = {};
    visited[0] = true;
    for (int i = 1; i < V;i++) {
        visited[i] = false;
    }

    std::vector<int> res {0};
    dfsGraph(0, adj, res, visited);
    return res;
}

int maxWeightCell(int n, std::vector<int> edges){

    std::map<int, int> weight_map = {};
    for (int index = 0; index < n; index ++ ) {
        int v = edges[index];
        if (v == -1){
            continue;
        }
        weight_map.insert_or_assign(v, 0);
        weight_map[v] += index;
    }

    int max_weight = 0;
    int best_index = n - 1;

    for (auto p = weight_map.begin(); p != weight_map.end(); p++) {
        int v = p -> first, w = p -> second;
        if (w >= max_weight) {
            max_weight = w;
            best_index = v;
        }
    }

    return best_index;
}


