from collections import deque

class Node:
    pass

class Node:
    def __init__(self, info, left: Node=None, right: Node=None) -> None:
        self.info = info
        # the children default to None
        self.left = left
        self.right = right


# we can't talk about depth first without the STACK Data Structure
def preOrder(root: None):
    if root is None:
        return []
    # define the stack
    to_do = deque()
    # append the root
    to_do.append(root)
    result = []
    while len(to_do) != 0:
        top_node = to_do.pop()
        result.append(top_node.info)
        if top_node.right:
            to_do.append(top_node.right)
        if top_node.left:
            to_do.append(top_node.left)

    print(" ".join([str(c) for c in result]))


class GNode:
    pass


class GNode:
    def __init__(self, data: int, adjacent_nodes: list[GNode]):
        self.data = data
        self.adjacent_nodes = adjacent_nodes


def build_graph(n: int, m: int, edges: list[list]):
    data_to_node = {}

    # first create the nodes
    for i in range(1, n + 1):
        data_to_node[i] = GNode(i, [])

    for edge in edges:
        data_to_node[edge[0]].adjacent_nodes.append(edge[1])
        data_to_node[edge[1]].adjacent_nodes.append(edge[0])

    return data_to_node


from collections import deque


def bfs(n, m, edges, s):
    # first create the damn graph
    data_to_node = build_graph(n, m, edges)

    # first create a dictionary for values
    nodes_distance = {}
    queue = deque()
    queue.append((s, 0))

    visited_nodes = {s}
    while len(queue) != 0:
        top_element, distance = queue.popleft()
        nodes_distance[top_element] = distance
        # extract the node corresponding to the value
        top_element_node = data_to_node[top_element]
        # add each adjacent node to the queue
        for node in top_element_node.adjacent_nodes:
            if node not in visited_nodes:
                queue.append((node, distance + 1))
                visited_nodes.add(node)

    for i in range(1, n + 1):
        if i not in nodes_distance:
            nodes_distance[i] = -1

    distances = sorted(nodes_distance.items(), key=lambda item: item[0])
    distances = [d[1] * 6 if d[1] != -1 else d[1] for d in distances]

    # remove the zero: representing the start value
    distances.remove(0)
    return distances


def main():
    n = 4
    m = 2
    edges = [[1, 2], [1, 3]]
    s = 1
    d = bfs(n, m, edges, s)


if __name__ == '__main__':
    main()




