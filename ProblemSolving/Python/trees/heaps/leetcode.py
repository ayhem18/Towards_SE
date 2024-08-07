
from typing import List
import heapq as hq


"""
https://neetcode.io/problems/kth-largest-integer-in-a-stream
"""
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.min_heap = []

        for n in nums: 
            self.add(n)        

    def add(self, val: int) -> int:
        
        n= len(self.min_heap)

        if n < self.k:
            hq.heappush(self.min_heap, val)
            # return the minimum element in the min heap
            return self.min_heap[0]

        if val > self.min_heap[0]:
            hq.heappop(self.min_heap)
            hq.heappush(self.min_heap, val)

        return self.min_heap[0]

"""
https://leetcode.com/problems/last-stone-weight/
"""
def lastStoneWeight(stones):
    # save all the stones in a heap
    h = [-x for x in stones]
    hq.heapify(h)
    while len(h) >= 2:
        x = -hq.heappop(h)
        y = -hq.heappop(h)
        if x > y:
            hq.heappush(h, y - x)

    return -h[0]


"""
https://leetcode.com/problems/k-closest-points-to-origin/
"""
class Point: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance_squared(self):
        return self.x ** 2 + self.y ** 2

    def __le__(self, other):
        return self.distance_squared() <= other.distance_squared()

    def __lt__(self, other):
        return self.distance_squared() < other.distance_squared()

    def __str__(self) -> str:
        return f"Point: ({self.x}, {self.y})"

def kClosest(points, k):
    pnts = [Point(p[0], p[1]) for p in points]
    res = hq.nsmallest(k, pnts)
    return [[r.x, r.y] for r in res]


"""
https://leetcode.com/problems/kth-largest-element-in-an-array/
"""
            
def findKthLargest(nums, k):
    min_heap = []
    assert k <= len(nums), "make sure k is not too large"
    for val in nums:
        n = len(min_heap)

        if n < k:
            hq.heappush(min_heap, val)
            continue
        
        if val > min_heap[0]:
            hq.heappop(min_heap)
            hq.heappush(min_heap, val)

    return min_heap[0]


"""
https://leetcode.com/problems/find-median-from-data-stream/
"""

class MedianFinder(object):

    def __init__(self):
        self.min_heap = []
        self.max_heap = []

    def addNum(self, num):
        n_max = len(self.max_heap)
        n_min = len(self.min_heap)
        
        if n_max == n_min + 1:
            # get the first value from the max_heap
            max_heap_root = -self.max_heap[0]
            if num >= max_heap_root:
                # the new value should be inserted in the upper half
                hq.heappush(self.min_heap, num)
            else:
                # the value is less than root of the max_heap, 
                hq.heappop(self.max_heap)
                hq.heappush(self.min_heap, max_heap_root)
                hq.heappush(self.max_heap, -num)

        elif n_max == n_min:
            if n_min == 0:
                hq.heappush(self.max_heap, -num)
                return 
            
            min_heap_root = self.min_heap[0]

            if num <= min_heap_root:
                # the new value should be inserted in the upper half
                hq.heappush(self.max_heap, -num)
            else:
                # the value is less than root of the max_heap, 
                hq.heappop(self.min_heap)
                hq.heappush(self.max_heap, -min_heap_root)
                hq.heappush(self.min_heap, num)


        else: 
            raise ValueError("Make sure the difference in sizes is as expected!!!")

    def findMedian(self):
        """
        :rtype: float
        """
        n_max = len(self.max_heap)
        n_min = len(self.min_heap)
        
        if n_max == n_min + 1:
            return -self.max_heap[0]
        elif n_max == n_min: 
            return (-self.max_heap[0] + self.min_heap[0]) / 2

        raise ValueError("Make sure the difference in sizes is as expected!!!")



"""
https://leetcode.com/problems/task-scheduler/

The task is supposedly solvable using a heap / PQ, but I could not figure out how to precisely use this DS. My solution passes the test. 
It hightly depends on the fact that the number of tasks is constant... so it is not scalable.
"""
class Task:
    def __init__(self, task_name, last_run_time, count) -> None:
        self.task_name = task_name
        self.last_run_time = last_run_time
        self.count = count
        self.available = True

    def __le__(self, other):
        if self.last_run_time == other.last_run_time: 
            return self.count > other.count
        return self.last_run_time <= other.last_run_time 

    def __lt__(self, other):
        if self.last_run_time == other.last_run_time:
            return self.count >= other.count
         
        return self.last_run_time < other.last_run_time

from collections import Counter
def leastInterval(tasks, n):
    ts = Counter(tasks)
    l = [Task(t, count=occ,last_run_time=-n) for t, occ  in ts.items()]
    timer = 1 
    while len(l) > 0:
        min_last_time = l[0].last_run_time
        for t in l:
            t.available = (timer - t.last_run_time) > n
            min_last_time = min(min_last_time, t.last_run_time)
        # find the next task
        # a task that is available with the largest count
        arg_next_task = max(range(len(l)), key=lambda x: int(l[x].available) * l[x].count)

        next_task = l[arg_next_task]
        if not next_task.available:
            # this means that all tasks are inavailable at this point
            # we should move time to the first timer for which at least one task is available
            timer = (min_last_time + n + 1) 
            continue
        
        next_task.count -= 1
        if next_task.count == 0:
            timer += 1
            del(l[arg_next_task])
            continue

        next_task.last_run_time = timer
        timer += 1

    return timer - 1



if __name__ == '__main__':
    pass
