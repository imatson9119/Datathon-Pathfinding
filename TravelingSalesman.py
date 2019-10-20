import matplotlib.pyplot as plt
import random as rand

# User guide:
# Use function greedyTravelingWithSwaps(nodes, startingNode)
# nodes is an adjacency matrix, in the form {0: [(0, 0), .. ,(n, distTonthNode)], 1: [(), .. , ()] ....}
# startingNode is the node to start at, can be in range [0, n]
# The return value returns order, distance
# order the an array that gives the order the nodes are visited
# distance gives the total cost to traverse through all nodes

# computes distance between 2 coordinates
def computeDist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)

# computes distance of entire ordering of cartesian coordinates
def computeTotalDist(order, points):
    dist = 0
    for i in range(len(order)-1):
        dist += computeDist(points[order[i]], points[order[i+1]])
    return dist


def visitNextNode(nodes, currentOrder, currentDistance, nodesVisited):
    if len(currentOrder) == len(nodes.keys()):
        return currentOrder, currentDistance
    else:
        min = 100000000
        closestNode = -1
        currentNode = currentOrder[-1]
        for t in nodes[currentNode]:
            if min > t[1] and not t[0] in nodesVisited and t[0] != currentNode:
                min = t[1]
                closestNode = t[0]
        currentDistance += min
        currentOrder += [closestNode]
        nodesVisited.add(closestNode)
        return visitNextNode(nodes, currentOrder, currentDistance, nodesVisited)

def reverseArray(arr):
    newArr = []
    for x in arr:
        newArr = [x] + newArr
    return newArr

def greedyTraveling(nodes, startingNode):
    nodesVisited = set()  # Keep track of nodes visited
    nodesVisited.add(startingNode)
    order, distance = visitNextNode(nodes, [startingNode], 0, nodesVisited)
    return order, distance

def performSwaps(order, nodes, distance, points = None):
    # Ignore the points value, that's for if we're testing the example using cartesian coordinates
    newOrder = order
    for i in range(len(newOrder)-2):
        for j in range(i+2, len(newOrder)-2):
            # o1 = computeDist(points[newOrder[j]], points[newOrder[j+1]]) + computeDist(points[newOrder[i]], points[newOrder[i+1]])
            # o2 = computeDist(points[newOrder[i]], points[newOrder[j]]) + computeDist(points[newOrder[i+1]], points[newOrder[j + 1]])
            o1 = nodes[newOrder[i]][newOrder[i+1]][1] + nodes[newOrder[j]][newOrder[j+1]][1]
            o2 = nodes[newOrder[i]][newOrder[j]][1] + nodes[newOrder[i+1]][newOrder[j+1]][1]
            # o1 = nodes[newOrder[i]][]
            if o2 < o1:
                distance -= (o1 - o2)
                newOrder[i + 1:j + 1].reverse()
                newOrder = newOrder[:i+1] + reverseArray(newOrder[i+1:j+1]) + newOrder[j+1:]
    return newOrder, distance


def greedyTravelingWithSwaps(nodes, startingNode):
    order, distance = greedyTraveling(nodes, startingNode)
    for i in range(5):
        order, distance = performSwaps(order, nodes, distance)
    return order, distance




def plotTSP(paths, points, num_iters=1):
    """
    path: List of lists with the different orders in which the nodes are visited
    points: coordinates for the different nodes
    num_iters: number of paths that are in the path list
    """
    print(paths)
    # Unpack the primary TSP path and transform it into a list of ordered
    # coordinates

    x = [];
    y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])

    plt.plot(x, y, 'co')

    # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
    a_scale = float(max(x)) / float(100)

    # Draw the older paths, if provided
    if num_iters > 1:

        for i in range(1, num_iters):

            # Transform the old paths into a list of coordinates
            xi = [];
            yi = [];
            for j in paths[i]:
                xi.append(points[j][0])
                yi.append(points[j][1])

            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]),
                      head_width=a_scale, color='r',
                      length_includes_head=True, ls='dashed',
                      width=0.001 / float(num_iters))
            for i in range(0, len(x) - 1):
                plt.arrow(xi[i], yi[i], (xi[i + 1] - xi[i]), (yi[i + 1] - yi[i]),
                          head_width=a_scale, color='r', length_includes_head=True,
                          ls='dashed', width=0.001 / float(num_iters))

    # Draw the primary path for the TSP problem
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale,
              color='g', length_includes_head=True)
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale,
                  color='g', length_includes_head=True)

    # Set axis too slitghtly larger than the set of x and y
    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()



if __name__ == "__main__":
    points = []
    nodes = {}
    spread = 100
    for i in range(8):
        for j in range(8):
            points += [(i * 13 + rand.randint(-1 * spread, spread) + 4, j * 13 + rand.randint(-1 * spread, spread) + 4)]
    points = []
    for i in range(80):
        points += [(rand.randint(0,100), rand.randint(0,100))]

    for i in range(len(points)):
        p1 = points[i]
        nodesToBeAdded = []
        for j in range(0, len(points)):
            nodesToBeAdded += [(j, computeDist(p1, points[j]), points[j])]
        nodes[i] = nodesToBeAdded


    # First try: Greedy algorithm, select the closest point

    order = [] # Order in which points are visited, we can use this to construct a visualization of our solution
    nodesVisited = set() # Keep track of nodes visited
    # Remember: Adj matrix is in form nodes[0] = [(nodeNumber, distToNode, point), ...]

    print("___ Testing greedy algorithm ___")
    order1, distance = greedyTraveling(nodes, 0)
    print("Order of nodes visited: ", order1)
    print("Total distance traversed (cost): ", distance)
    print('\n', "___ Testing greedy with swaps ___")
    order2, distance = greedyTravelingWithSwaps(nodes, 0)
    print("Order of nodes visited: ", order2)
    print("Total distance traversed (cost): ", distance)

    paths = [order1, order2]

    plotTSP([paths[0]], points, 1)
    plotTSP([paths[1]], points, 1)

