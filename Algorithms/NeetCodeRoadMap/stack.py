"""
In this script, I solve the problems suggested by NeetCode road map for stack problems.
https://neetcode.io/roadmap
"""

# let's start by an easy one:
# valid parentheses: https://leetcode.com/problems/valid-parentheses/

from collections import deque


class Solution:
    def isValid(self, s: str) -> bool:
        # check if a string has valid parentheses
        o = ["{", "(", "["]
        c = ["}", ")", "]"]
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

    # the 4th task is a bit more interesting:
    # generating all the combinations of n parenthesis
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
        sub = {1: ["()"]}
        # fill the subs with the valid combination of lower values
        for i in range(2, n + 1):
            sub[i] = self.n_parenthesis_with_subs(i, sub)
        return list(sub[n])

    # The 5th task is quite cool, not gonna lie
    # https://leetcode.com/problems/daily-temperatures/
    def dailyTemperatures(self, temps: list[int]) -> list[int]:
        # let's initialize the array with the answers with all zeros
        ans = [0 for _ in temps]
        # initialize a stack
        stack = deque()
        for index, value in enumerate(temps):
            if len(stack) == 0 or ans[stack[-1]] >= value:
                stack.append(index)
            else:
                while True:
                    flag = len(stack) > 0 and temps[stack[-1]] < value
                    if not flag:
                        break
                    ans[stack[-1]] = index - stack[-1]
                    stack.pop()
                # at the end, add the current index
                stack.append(index)
        return ans


# the 2nd task is to build a stck data structure with some extra functionalities
#: and it worked from the 1st run!!
class MinStack:

    def __init__(self):
        self.s = deque()
        # any value that can be seen as a minimum value at one point will be saved in this stack
        self.min_s = deque()

    def push(self, val: int) -> None:
        # first thing add the value to the hidden stack
        self.s.append(val)
        # now we should check whether this value should be added to the minimum stack
        if len(self.min_s) == 0 or self.min_s[-1] >= val:
            # or equal is necessary in case there are multiple occurrences of the minimal values
            self.min_s.append(val)

    def pop(self) -> None:
        last_value = self.s[-1]

        if last_value == self.min_s[-1]:
            # remove the last min element
            self.min_s.pop()

        # remove the element from the stack anyway
        self.s.pop()

    def top(self) -> int:
        return self.s[-1]

    def getMin(self) -> int:
        return self.min_s[-1]


if __name__ == '__main__':
    s = Solution()
    print(s.dailyTemperatures([30, 30, 30]))
