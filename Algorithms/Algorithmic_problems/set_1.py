from collections import deque


class Solution:
    def binary_search(self, array: list, x, low, high):
        while low <= high:

            mid = low + (high - low) // 2

            if array[mid] == x:
                return mid

            elif array[mid] < x:
                low = mid + 1

            else:
                high = mid - 1

        return -1

    def two_sum(self, nums: list[int], target: int) -> list[int]:
        """
        Given an array of numbers, find the indices of the pair of values whose sum is equal to target
        The assumption is that such pair appears exactly once in "nums" array
        :param nums:  of values
        :param target: the
        :return:
        """
        # The solution passed the tests!!!! GREAT

        # first sort the array of values
        sorted_nums = sorted(nums)
        length = len(nums)
        res = []
        for index, n in enumerate(nums):
            # this means the pair was found
            if self.binary_search(sorted_nums, target - n, low=index, high=length - 1) != -1:
                # there are two possibilities when entering this block of code
                # first the bad one: target / 2 is present once and the conditional above can't detect it
                # loop through the indices of the original list
                for i in range(len(nums)):
                    if nums[i] == n and len(res) == 0:
                        res.append(i)
                    elif nums[i] == target - n and i not in res:
                        res.append(i)
                        return res
                # if this part of the code is reached: it means the pair found was indeed a false alarm
                res.clear()
        return [-1, -1]

    def two_sum_2(self, nums: list[int], target: int) -> list[int]:
        # this solution beats up ~62% speed-wise, but it is in the last 6.51% percentile memory-wise
        values_indices = {}
        for index, val in enumerate(nums):
            if val not in values_indices:
                values_indices[val] = [index]
            else:
                values_indices[val].append(index)
        for n in nums:
            if target - n in values_indices:
                if target - n != n:
                    return [values_indices[n][0], values_indices[target - n][0]]
                else:
                    if len(values_indices[n]) > 1:
                        return [values_indices[n][0], values_indices[n][1]]

        return [-1, -1]

    def lengthOfLongestSubstring(self, s: str) -> int:
        # first let's define the start and end parameters
        start = 0
        best_start, best_end = 0, 0
        current_dict = {}
        for i, char in enumerate(s):
            # first check if the char is seen for the first time
            if char not in current_dict:
                current_dict[char] = i
            else:
                # first check if the best start and ends should be updated
                if i - 1 - start > best_end - best_start:
                    best_end = i - 1
                    best_start = start
                # now we need to update the start
                # the new start position is the position of the previous occurrence of the character char + 1

                new_start = current_dict[char] + 1

                for j in range(start, new_start):
                    del current_dict[s[j]]

                start = new_start
                # the value of i-th character should be added
                current_dict[char] = i

        # check the if the substring ends at the end of the string
        if len(s) - 1 - start > best_end - best_start:
            best_end = len(s) - 1
            best_start = start

        return best_end - best_start + 1

    # let's get this valid parentheses question
    def isValid(self, s: str) -> bool:
        # check if a string has valid parentheses
        o = ["{", "(", "["]
        c = ["{", "(", "["]
        open_parentheses = set(o)
        close_parentheses = set(c)
        parentheses = dict(zip(c, o))

        # create a hidden deque
        if len(s) == 0:
            return True

        stack = deque()
        for char in s:
            if char in open_parentheses:
                stack.append(char)
            if char in close_parentheses:
                # check if the closing parentheses correspond to the more recent opening parenthesis
                if len(stack) > 0 and parentheses[char] == stack[-1]:
                    stack.pop()
                else:
                    return False

        # the stack must be empty by the end of the string
        return len(stack) == 0

    # well spotting a string with valid parentheses is a child's game

    def n_parenthesis_with_subs(self, n: int, sub: dict):
        # this assumes that the sub dictionary have the valid combinations for all values from 1 to n - 1
        results = set(["(" + s + ")" for s in sub[n - 1]])
        for i in range(1, n):
            s1 = sub[i]
            s2 = sub[n - i]
            results.update([l1 + l2 for l1 in s1 for l2 in s2])
        return list(results)

    def generateParenthesis(self, n: int) -> list[str]:
        # create a dictionary
        sub = {}
        sub[1] = ["()"]
        # fill the subs with the valid combination of lower values
        for i in range(2, n + 1):
            sub[i] = self.n_parenthesis_with_subs(i, sub)
        return list(sub[n])


def main():
    sol = Solution()
    n = 4
    print(sol.generateParenthesis(n))


if __name__ == "__main__":
    main()
