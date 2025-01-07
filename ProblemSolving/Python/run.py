import random
import numpy as np
from tqdm import tqdm

from utils import random_array
from arrays.arrays import sort_array_with_known_elements
from backtracking.medium import numberOfPath, numberOfPathBacktracking
from arrays.ad_hoc import find3Numbers
from arrays.sorting import minSwaps

from mathy.file1 import rotate_constant_space, rotate_linear_space, subarraySum 
from trees.utils_trees import Node, tree_array_rep
from trees.basic_depth_recursion import findNodeAndParent, IsFoldable, lca
from trees.level_traversal import isCousins, isPerfect, isCompleteBT, dupSub, reverseLevelOrder, zigZagTraversal, getMaxSum, minTime, treePathSum
from trees.traversal import constructBinaryTree, preorder_traversal, inOrder

# testing the inplace rotation algorithm based on ideas from number theory

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

# checking the code to convert a tree from the Node representation to the array representation
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

# some function to check some backtracking problem
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


# adhoc probblems
def adhoc_array():
    a = [1, 2, 2, 2, 2, 1, 2, 0, 1, -1]
    print(find3Numbers(a))

# mathy array problems
def mathy_arrays():
    arr = [1, 2, 3,]
    print(subarraySum(arr))
    print(subarraySum([0, 1]))    

def sorting_arrays():
    a = [1, 2, 3, 4]
    print(minSwaps(a))

    a = [1, 3, 2, 4]
    print(minSwaps(a))

    a = [1, 3, 4, 2, 5, 7, 8, 9, 6]
    print(minSwaps(a))

    a = [1, 3, 4, 2, 5, 7, 8, 9, 6, 10, 11, 12]
    print(minSwaps(a))

    a = [1, 2, 5, 3, 4, 6, 10, 9, 8, 7]
    print(minSwaps(a))


def getTree() -> Node:
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
    n2.right = n5

    n4.left = n6
    n4.right = n7

    n5.left = n8
    n5.right = n9

    n10 = Node(10)
    n3.left = n10
    n10.left = Node(11)

    return n1


def trees1():
    n1 = getTree()

    values = list(range(1, 10))

    d = findNodeAndParent(n1, values)

    for k, v in d.items():
        for n in v:
            c, p = n
            if p is not None:
                print(f"child: {c.data}, parent: {p.data}")
            else:
                print(f"child: {c.data}, parent: {p}")

        print("#" * 10)


def trees2():
    n1 = getTree()
    pos_pairs = [(6, 8), (7, 9), (10, 4), (10, 5), (11, 7), (11, 9), (11, 6)]

    for v1, v2 in pos_pairs:
        assert isCousins(n1, v1, v2), "positive pairs not detected"
        assert isCousins(n1, v2, v1), "positive pairs not detected"


    neg_pairs = [(6, 7), (8, 9), (1, 2), (1, 3), (11, 10), (3, 4)]

    for v1, v2 in neg_pairs:
        assert not isCousins(n1, v1, v2), "neg pairs  detected"
        assert not isCousins(n1, v2, v1), "neg pairs detected"



def trees3():
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    
    n1.left = n2
    n1.right = n3

    print(IsFoldable(n1))


    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)

    n1.left = n2
    n2.left = n3

    n1.right = n4
    n4.right = n5

    print(IsFoldable(n1))

    n6 = Node(6)
    n7 = Node(7)

    n3.right = n6
    n5.left =  n7

    print(IsFoldable(n1))

    n8 = Node(8)
    n9 = Node(9)

    n6.left = n8
    n7.left = n9
    
    print(IsFoldable(n1))



def trees4():
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)

    print(inOrder(n1))

    n1.left = n2
    n1.right = n3

    print(inOrder(n1))

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)

    n1.left = n2
    n1.right = n3
    n2.left = n4
    n2.right = n5
    n5.left = n6

    print(inOrder(n1))


    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)

    n1.left = n2
    n2.left = n3
    n3.left = n4
    n4.left = n5
    n5.right = n6

    print(inOrder(n1))    



if __name__ == '__main__':
    random.seed(0)
    np.random.seed(0)  
    trees4()

