#ifndef CPP_PREFIXSUM_H
#define CPP_PREFIXSUM_H

# include <vector>


void update(int a[], int n, int updates[], int k);
int equilibriumPoint(long long arr[], int n);
bool subArrayExists(int arr[], int n);
int longSubarrWthSumDivByK(int arr[], int n, int k);
std::vector<int> subarraySum(std::vector<int>& arr, int n, long long s);

#endif //CPP_PREFIXSUM_H