## let's put what I just learnt to test by solving some DP problems on HACKER RANK
## starting by a fairly simple one: https://www.hackerrank.com/challenges/coin-change/problem?isFullScreen=true

def get_num_ways(n: int, coins: list[int]) -> int:
    # first base case: if there are no coins
    # or simply n is less than the smallest coin
    if len(coins) == 1:
        return int(n % coins[0] == 0)

    if len(coins) == 0:
        return 0

    count = 0  # the count should start 1 if n is divisible by coins[0]
    for i in range(int(n / coins[0]) + 1):
        count += get_num_ways(n - i * coins[0], coins[1:])

    return count


# the recursive function will end up exceeding the time limit, so let's make a memoized version
def get_num_ways_memo(n: int, coins: list[int], memo: dict = None):
    if memo is None:
        memo = {}

    # first check if the combination of n and the largest value was seen before
    if len(coins) == 0:
        return 0

    key = (n, coins[0])
    if key in memo:
        return memo[key]

    if len(coins) == 1:
        return int(n % coins[0] == 0)

    count = 0
    for i in range(int(n / coins[0]) + 1):
        count += get_num_ways_memo(n - i * coins[0], coins[1:], memo=memo)
    # save the result in the memo
    memo[key] = count
    return memo[key]


# the memoization version passes all tests!!!
def getWays(n: int, coins: list[int]) -> int:
    # coins: represents coin values, n: amount of money
    # in how many ways can we represent n as a linear sum of the values in the 'coins' variable
    # 1st step is to make sure the coins are unique and sorted descendingly
    if n == 0:
        return 0

    coins = sorted(list(set(coins)), reverse=True)
    return get_num_ways_memo(n, coins)


# let's consider a different problem: https://www.hackerrank.com/challenges/equal/problem?isFullScreen=true
# given an array of values, at each round we add either 1, 2, 5 to all elements but one element
# all elements are equal. We need to find the minimum number of rounds

# let's start with a good function:


def min_combination(n: int, components: list[int] = None) -> dict:
    # make sure components is sorted ascendingly
    if components is None:
        components = [5, 2, 1]  # the values of the problem as given in hacker rank
    frequency = {}
    for v in components:
        frequency[v] = int(n / v)
        n = n - frequency[v] * v

    return frequency


def add_all_but_one(array: list[int], index: int, add_value: int) -> list[int]:
    return [v + (i != index) * add_value for i, v in enumerate(array)]


def min_rounds(values: list[int]) -> int:
    if len(values) <= 1:
        return 0

    # first thing create the differences array
    differences = [values[i + 1] - values[i] for i in range(len(values) - 1)]

    # we reach the state where all elements are the same
    if all([d == 0 for d in differences]):
        return 0

    memo = {}
    # values must be sorted ascendingly
    for i in range(len(values) - 1):
        diff = values[i + 1] - values[i]
        assert diff >= 0
        if diff == 0:
            continue
        # get the number of rounds of 1, 2, and 5
        rounds_freqs = min_combination(diff)
        # get the total number of rounds: the sum of the frequencies
        total_num_rounds = sum(rounds_freqs.values())
        new_array = add_all_but_one(values, i + 1, diff)
        return total_num_rounds + min_rounds(new_array)


def equal(values: list[int]):
    # make sure to have values sorted
    values = sorted(values)
    return min_rounds(values)


if __name__ == '__main__':
    for i in range(50):
        print(i, min_combination(i), sep=':\t')
