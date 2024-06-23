# include <vector>


std::vector<std::vector<int>> allSubsetsN(const std::vector<int> & set, int N) {
    if (N == 0) {
        return {{}};
    }
    auto subSubsets = allSubsetsN(set, N - 1);
    std::vector <std::vector<int>> res {subSubsets.size()};
    for (int i = 0; i < res.size(); i++) {
        res[i] = subSubsets[i];
    }

    for (auto &v : subSubsets) {
        v.push_back(set[N - 1]);
        res.push_back(v);
    }
    return res;
}

std::vector<std::vector<int>> allSubsets(const std::vector<int> & set) {
    return allSubsetsN(set, static_cast<int> (set.size()));
}
