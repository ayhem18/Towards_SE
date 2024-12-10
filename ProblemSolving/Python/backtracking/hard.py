"""
This script contains my solutions for some "hard" backtracking problems on geeks for geeks 

Ps: the categorization of problems isn't that reliable...
"""

# https://www.geeksforgeeks.org/problems/word-break-part-23249/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card

from typing import Union

def wordBreakList(words: Union[dict, set], string: str) -> list[list[str]]:
    # the performance can be improved by saving the results at each index of the original string
    # dp style basically (or even the substring itself...)

    final_results = []

    if not isinstance(words, (dict, set)):
        words = dict(words)

    current_word = ""

    possible_first_words = []

    for i, c in enumerate(string):
        current_word += c
        if current_word in words:
            possible_first_words.append(current_word)

    if len(possible_first_words) == 0:
        return []

    for fw in possible_first_words:
        if fw == string:
            final_results.append([fw])
            continue 

        intermediate_results = wordBreakList(words, string[len(fw):])

        # this means this path fails somewhere down the line
        if len(intermediate_results) == 0:
            continue
            
        final_results.extend([[fw] + r for r in intermediate_results])

    return final_results

def wordBreak(words: Union[dict, set], string: str) -> list[str]:
    return [" ".join(r) for r in wordBreakList(words, string)]


