import random
import numpy as np
from tqdm import tqdm

from utils import random_array
from arrays.arrays import sort_array_with_known_elements
from mathy.file1 import rotate_constant_space, rotate_linear_space 

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


from trees.gfg.easy import Node, tree_array_rep

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


from backtracking.medium import numberOfPath, numberOfPathBacktracking

def check_bt():
    arr = [
        [1, 2, 3], 
        [4, 6, 5], 
        [9, 8, 7]
        ]

    for i in range(5, 30):
        s1, s2 = numberOfPathBacktracking(n=len(arr), k=i, arr=arr), numberOfPath(n=len(arr), k=i, arr=arr)
        assert s1 == s2
        

    arr = [
        [1, 2, 3], 
        [4, 6, 5], 
        [3, 2, 1]
        ]


    for i in range(5, 20):
        s1, s2 = numberOfPathBacktracking(n=len(arr), k=i, arr=arr), numberOfPath(n=len(arr), k=i, arr=arr)
        assert s1 == s2

from arrays.twoPointers import closestToZero, segregate0and1
from arrays.prefixArray import longestCommonSum
from arrays.hash_map_set import removeDuplicates

def farray():
    print(removeDuplicates([0, 0, 0, 0, 0]))
    print(removeDuplicates([0, 1, 2, 3, 4]))

from arrays.ad_hoc import rearrangeArray, find3Numbers

def adhoc_array():
    # a = [1, 4, 1, 1, 2, 3]
    # print(find3Numbers(a))
    # a = [5, 4, 3, 2, 4, 3, 5, 1, 2]
    # print(find3Numbers(a))

    a = [1, 2, 2, 2, 2, 1, 2, 0, 1, -1]
    print(find3Numbers(a))


from mathy.file1 import subarraySum 

def mathy_arrays():
    arr = [1, 2, 3,]
    print(subarraySum(arr))
    print(subarraySum([0, 1]))    


if __name__ == '__main__':
    random.seed(0)
    np.random.seed(0)  
    adhoc_array()    