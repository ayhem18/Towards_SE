# noinspection PyMethodMayBeStatic
class Solution:
    # well it is sad that I am not always capable for directly solving an easy problem
    def maxProfit(self, prices: list[int]) -> int:
        if len(prices) < 2:
            return 0
        min_v, max_p = prices[0], 0
        for v in prices[1:]:
            min_v = min(v, min_v)
            max_p = max(max_p, v - min_v)

        return max_p

    # not gonna lie, quit proud of this solution: beats 99.5% performance wise and 100% memory-wise
    # https://leetcode.com/problems/longest-substring-without-repeating-characters/submissions/
    def lengthOfLongestSubstring(self, s: str) -> int:
        # first let's define the start and end parameters
        if len(s) == 0:
            return 0

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
                # the new start position is the position of the previous occurrence of the
                # character char + 1

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

    # the following block of functions is for the task:
    # https://leetcode.com/problems/longest-repeating-character-replacement/
    # my solution isn't the best, but it passes...
    def longest_new_seq(self, blocks: list[int], links: list[int], links_limit: int) -> int:
        assert len(blocks) == len(links) + 1, "MAKE SURE THE LENGTHS ARE AS EXPECTED"
        if len(blocks) == 1:
            return blocks[0] + links_limit

        # the idea is to find the longest sequence, by adding at most 'links_limit' link between the blocks
        start, end, length, count = 0, 1, blocks[0], 0
        max_length = 0

        while end < len(blocks):
            if length == 0:
                length = blocks[end]
                end += 1

            while end < len(blocks):
                length += blocks[end] + links[end - 1]
                count += links[end - 1]
                if count > links_limit:
                    break
                end += 1

            if count > links_limit:
                # calculate the actual length used in this window
                length -= (blocks[end] + links[end - 1])
                # calculate the actual count too
                count -= links[end - 1]

            # keep in mind that 2 lengths can be achieved using different number of links
            # the links that were not used should be added to the length of the resulting sequence
            final_length = length + (links_limit - count)
            if final_length > max_length:
                max_length = final_length

            # if we reached the last block, no further processing is needed
            if end < len(blocks):
                # should keep in mind that if start = end - 1
                # then the link should not be removed here

                length -= (blocks[start] + (links[start] if end > start + 1 else 0))
                # calculate the actual count too
                count -= (links[start] if end > start + 1 else 0)
            start += 1

        return max_length

    def __build_blocks_and_links(self, values: list[int]):
        blocks = [[values[0]]]
        links = []
        last_value = values[0]
        for v in values[1:]:
            if v > last_value + 1:
                blocks[-1] = len(blocks[-1])
                links.append(v - last_value - 1)
                blocks.append([v])
            else:
                blocks[-1].append(v)
            last_value = v

        if isinstance(blocks[-1], list):
            blocks[-1] = len(blocks[-1])

        return blocks, links

    def characterReplacement(self, string: str, limit: int) -> int:
        char_to_indices = {}
        for index, char in enumerate(string):
            if char not in char_to_indices:
                char_to_indices[char] = set()
            # add the index to the set
            char_to_indices[char].add(index)

        # sort the indices in each value
        for k, v in char_to_indices.items():
            char_to_indices[k] = sorted(list(v))

        # find the blocks and links for each
        max_length = 0
        for k, v in char_to_indices.items():
            blocks, links = self.__build_blocks_and_links(v)
            max_len = self.longest_new_seq(blocks, links, limit)
            max_length = max(max_len, max_length)

        return min(max_length, len(string))

    # this one should be slightly better
    # https://leetcode.com/problems/permutation-in-string/
    # pass from the first try beating 90% of solutions...
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # first let's rule some degenerate cases
        if len(s1) > len(s2):
            return False

        occurrences = {}
        for char in s1:
            if char not in occurrences:
                occurrences[char] = 0
            occurrences[char] -= 1

        # time to check if the first len(s1) characters in s2 are indeed a permutation of s1
        for char in s2[:len(s1)]:
            if char not in occurrences:
                occurrences[char] = 0

            occurrences[char] += 1

            if occurrences[char] == 0:
                del(occurrences[char])

        if len(occurrences) == 0:
            return True

        for end in range(len(s1), len(s2)):
            c_end = s2[end]
            c_start = s2[end - len(s1)]
            # first add c_end
            if c_end not in occurrences:
                occurrences[c_end] = 0

            occurrences[c_end] += 1
            if occurrences[c_end] == 0:
                del (occurrences[c_end])
            # remove c_start

            if c_start not in occurrences:
                occurrences[c_start] = 0

            occurrences[c_start] -= 1
            if occurrences[c_start] == 0:
                del (occurrences[c_start])

            if len(occurrences) == 0:
                return True

        return False


if __name__ == '__main__':
    s = Solution()
    s1 = 'abbba'
    s2 = 'aabbaaabbab'
    print(s.checkInclusion(s1, s2))