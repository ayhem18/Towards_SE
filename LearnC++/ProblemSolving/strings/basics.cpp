# include <string>
# include <vector>
std::string reverseWords(std::string S)
{
    std::vector<int> indices = {};
    for (int i = 0; i < S.size(); i ++ ){
        if (S.at(i) == '.') {
            indices.push_back(i);
        }
    }

    int last_index = indices[indices.size() - 1];
    std::string rev {S.substr(last_index, S.size() - last_index)};
    for (auto a = indices.rend(); a != (indices.rend() - 1); a ++) {
        rev.push_back('.');
        rev.append(S.substr(*a, *(a + 1) - *a));
    }

    rev.append(S.u)
}
