import random
import numpy as np
from typing import List

from tqdm import tqdm
from graphs import neetcode as nc

from hashing.test_hash import test_first_not_repeat_char
from hashing.gfg1 import findLongestConseqSubseq, getPairsCount, firstRepeated, maxLen,canPair, encode, decode
from twoPointers.Tpnts2 import maxArea, trap

from slidingWindow.sw1 import longestUniqueSubsttr, countDistinct, smallestSubWithSum
from div_and_con.dc1 import searchMatrix, findMin
from utils import random_array
from arrays.arrays import rotate_constant_space, rotate_linear_space, sort_array_with_known_elements

def test_constant_space_array_rotation():
    for _ in tqdm(range(1000)):
        n = random.randint(1, 1000)
        # k = random.randint(1, 10 ** 5)

        a = random_array(n, 0, 1000)
        
        for k in range(1, len(a)):
            a_rotated = a.copy()
            rotate_constant_space(a_rotated, k=k)
            a_rotated_correct = rotate_linear_space(a, k=k)

            assert a_rotated_correct == a_rotated, "code doesn't work"

def test_sorting_array_with_known_elements():
    for _ in tqdm(range(1000)):
        n0, n1, n2 = random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)

        zeros, ones, twos = [0 for _ in range(n0)], [1 for _ in range(n1)], [2 for _ in range(n2)]
        array = []
        array.extend(zeros)
        array.extend(ones)
        array.extend(twos)

        np.random.shuffle(array)

        sort_array_with_known_elements(array)

        sorted_array = sorted(array)

        assert sorted_array == array, "code does not work"


from trees.gfg.easy import Node, tree_array_rep, isSymmetric, diameter, isBalanced, largestValues, kthLargest, zigZagTraversal, inorderSuccessor


def check_trees2array():
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)

    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)

    n7 = Node(7)
    n8 = Node(8)
    n9 = Node(9)

    # setting 1
    n1.left = n2
    n1.right = n3    
    n2.left = n4
    n2.right = n5
    n3.left = n6
    n3.right = n7
    n4.left = n8
    n4.right = n9
    print(tree_array_rep(n1))

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)

    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)

    n7 = Node(7)
    n8 = Node(8)
    n9 = Node(9)

    n1.left = n2
    n2.left = n3
    n3.left = n4

    print(tree_array_rep(n1))

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)

    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)

    n7 = Node(7)
    n8 = Node(8)
    n9 = Node(9)

    n1.left = n2
    n1.right = n3

    n2.left = n4
    n3.right = n5

    print(tree_array_rep(n1))

def testSymmetrie():

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(2)

    n1.left = n2
    n1.right = n3

    print(isSymmetric(n1))

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(2)

    n4 = Node(1)
    n5 = Node(1)

    n6 = Node(1)
    n7 = Node(1)

    n1.left = n2
    n1.right = n3

    n2.right = n4
    n3.left = n5

    n2.left = n6
    n3.right = n7

    print(isSymmetric(n1))


def check_depth():
    n10 = Node(10)
    n5 = Node(5)
    n4 = Node(4)
    n8 = Node(8)

    n12 = Node(12)
    n11 = Node(11)
    n20 = Node(20)

    # print("#" * 10)
    n10.left = n5
    n5.left = n4
    n5.right = n8

    n10.right = n12
    n12.left = n11
    n12.right = n20


    n2 = Node(2)
    n1 = Node(1)
    n3 = Node(3)

    n2.left = n1
    n2.right = n3

    val = inorderSuccessor(n2, n2)
    if val is not None:
        print(val.data)

    # print(inorderSuccessor(n10, n8))
    # print(inorderSuccessor(n10, n20))
    # print(inorderSuccessor(n10, n11))





if __name__ == '__main__':
    random.seed(0)
    np.random.seed(0)
    # test_constant_space_array_rotation()
    # test_sorting_array_with_known_elements()  
    
    # check_trees2array()
    # testSymmetrie()
    check_depth()
