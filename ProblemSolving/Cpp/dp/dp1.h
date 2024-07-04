#ifndef CPP_DP1_H
#define CPP_DP1_H

# include "../utils.h"
// let's start simple with fibonacci

long long int topDown(int n);

long long int bottomUp(int n);

long long int count(int coins[], int N, int sum);

bool isSubsetSum(std::vector<int>&arr, int sum);

lli _countWays(int n, int k);

lli _countWaysDP(int n, int k);


int minCoins(std::vector<int> &coins, int n, int sum);

int lcs(int n, int m, std::string& str1, std::string& str2);

std::string smallestWindow (std::string& s, std::string& p);

#endif //CPP_DP1_H
