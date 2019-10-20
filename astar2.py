import numpy as np
import time
from heapq import *
import sys

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, cost=0):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closedDict = {}

    # Add the start node
    heappush(open_list,start_node)
    # Loop until you find the end
    startTime = time.time()
    while open_list:
        #sleep(0.2)
        # Get the current node
        current_node = heappop(open_list)

        if time.time() - startTime > 4:
            return stupidSearch(maze, start, end)

        # Pop current off open list, add to closed list
        #closed_list.append(current_node)
        #print(num_it, current_node.position, current_node.on_list, current_node.g)
        #current_node.on_list = True
        closedDict[current_node.position] = 0
        # print(current_node.h)
        # Found the goal
        #print('open list:', [i.position for i in open_list])
        #print('closed list:',[i.position for i in closed_list])
        # print(current_node.position, '=', end_node.position)
        if current_node.position == end_node.position:
            end_cost = current_node.g
            path = []
            current = current_node
            while current is not None:
                path.append([tuple(reversed(current.position)), current.cost])
                current = current.parent
            print('returning')
            return path[::-1], end_cost   # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1, 1), (0, 1, 1), (-1, 0, 1), (1, 0, 1)]:  # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            node_value = maze[node_position[0]][node_position[1]]
            if node_value == np.inf:
                continue

            # Create new node
            new_node = Node(current_node, node_position, node_value)

            # Append
            children.append(new_node)
        # END CHILDREN GENERATION

        # Loop through children
        for child in children:
            cont = False
            # Child is on the closed list
            '''for closed_child in closed_list:
                if child.position == closed_child.position:
                    cont = True
                    continue
            if cont:
                continue'''

            #if child.on_list:
             #   continue

            if child.position in closedDict.keys():
                continue

            # Create the f, g, and h values
            child.g = current_node.g + child.cost
            child.h = (((child.position[0] - end_node.position[0]))**2 + (
                        (child.position[1] - end_node.position[1]))**2)
            child.f = child.g + 100 * child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    cont = True

                    continue
            if cont:
                continue
            # Add the child to the open list
            heappush(open_list, child)

def stupidSearch(maze, start, end):
    sys.setrecursionlimit(10000)
    #start = tuple(reversed(start))
    #end = tuple(reversed(end))
    x1 = start[1]
    y1 = start[0]
    x2 = end[1]
    y2 = end[0]
    print("GOTO")
    print(start, end)
    time.sleep(0.1)
    path = []
    cost = 0
    while x1 != x2 or y1 != y2:
        # Try to optimize y
        dir = -1 # 0 = L, 1 = U, 2 = R, 3 = D
        if y1 < y2:
            x1,y1,x2,y2 = move_up(path, maze, (x1, y1), (x2, y2))
        elif y1 > y2:
            x1,y1,x2,y2 = move_down(path, maze, (x1,y1), (x2, y2))

        if x1 < x2:
            x1,y1,x2,y2 = move_right(path, maze, (x1, y1), (x2, y2))
        elif x1 > x2:
            x1,y1,x2,y2 = move_left(path, maze, (x1, y1), (x2, y2))
    print("Stupid:", path)
    return path, cost

def move_up(path, maze, start, end, flag=""):
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]
    while y1 != y2 or flag != "":
        if flag == "D":
            if 0 <= y1 - 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1-1][x1] != np.inf:
                return x1, y1, x2, y2
        if flag == "L":
            if 0 <= y1 < len(maze) and 0 <= x1 - 1 < len(maze[0]) and maze[y1][x1-1] != np.inf:
                return x1,y1, x2,y2
        if flag == "R":
            if 0 <= y1 < len(maze) and 0 <= x1 + 1 < len(maze[0]) and maze[y1][x1 + 1] != np.inf:
                return x1,y1,x2,y2

        if not(0 <= y1 + 1 < len(maze) and 0 <= x1 < len(maze[0])) or maze[y1 + 1][x1] == np.inf:
            if x1 < x2 and 0 <= y1 < len(maze) and 0 <= x1 + 1 < len(maze[0]) and maze[y1][x1+1] != np.inf:
                x1, y1, x2, y2 = move_right(path, maze, (x1, y1), (x2, y2), "U")
                print("After recursive call:", x1,y1,x2,y2)
                #time.sleep(5)
                continue
            elif x1 >= x2 and maze[y1][x1-1] != np.inf:
                x1, y1, x2, y2 = move_left(path, maze, (x1, y1), (x2, y2), "U")
                continue
        y1 += 1
        print(x1, y1, "\t", x2, y2)
        path.append([(x1, y1), maze[y1][x1]])
    return x1,y1,x2,y2

def move_down(path, maze, start, end, flag=""):
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]
    while y1 != y2 or flag != "":
        if flag == "U":
            if 0 <= y1 + 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1+1][x1] != np.inf:
                return x1, y1, x2, y2
        if flag == "L":
            if 0 <= y1 < len(maze) and 0 <= x1-1 < len(maze[0]) and maze[y1][x1-1] != np.inf:
                return x1,y1, x2,y2
        if flag == "R":
            if 0 <= y1 < len(maze) and 0 <= x1 + 1 < len(maze[0]) and maze[y1][x1 + 1] != np.inf:
                return x1,y1,x2,y2

        if not(0 <= y1 - 1 < len(maze) and 0 <= x1 < len(maze[0])) or maze[y1 - 1][x1] == np.inf:
            if x1 < x2 and 0 <= y1 < len(maze) and 0 <= x1 + 1 < len(maze[0]) and maze[y1][x1 + 1] != np.inf:
                x1, y1, x2, y2 = move_right(path, maze, (x1, y1), (x2, y2), "D")
                continue
            elif x1 >= x2 and 0 <= y1 < len(maze) and 0 <= x1 - 1 < len(maze[0]) and maze[y1][x1-1] != np.inf:
                x1, y1, x2, y2 = move_left(path, maze, (x1, y1), (x2, y2), "D")
                continue
        y1 -= 1
        print(x1, y1, "\t", x2, y2)
        path.append([(x1, y1), maze[y1][x1]])
    return x1,y1,x2,y2

def move_left(path, maze, start, end, flag=""):
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]
    while x1 != x2 or flag != "":
        if flag == "D":
            if 0 <= y1 - 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1-1][x1] != np.inf:
                return x1, y1, x2, y2
        if flag == "U":
            if 0 <= y1 + 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1 + 1][x1] != np.inf:
                return x1,y1, x2,y2
        if flag == "R":
            if 0 <= y1 < len(maze) and 0 <= x1 + 1 < len(maze[0]) and maze[y1][x1 + 1] != np.inf:
                return x1,y1,x2,y2

        if not(0 <= y1 < len(maze) and 0 <= x1 - 1 < len(maze[0])) or maze[y1][x1 - 1] == np.inf:
            if y1 < y2 and 0 <= y1 + 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1+1][x1] != np.inf:
                x1, y1, x2, y2 = move_up(path, maze, (x1, y1), (x2, y2), "L")
                continue
            elif y1 >= y2 and 0 <= y1 - 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1 - 1][x1] != np.inf:
                x1, y1, x2, y2 = move_down(path, maze, (x1, y1), (x2, y2), "L")
                continue
        x1 -= 1
        print(x1,y1, "\t", x2,y2)
        path.append([(x1, y1), maze[y1][x1]])
    return x1,y1,x2,y2

def move_right(path, maze, start, end, flag=""):
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]
    while x1 != x2 or flag != "":
        if flag == "D":
            if 0 <= y1 - 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1 - 1][x1] != np.inf:
                return x1, y1, x2, y2
        if flag == "U":
            if 0 <= y1 + 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1 + 1][x1] != np.inf:
                return x1, y1, x2, y2
        if flag == "L":
            if 0 <= y1 < len(maze) and 0 <= x1 - 1 < len(maze[0]) and maze[y1][x1 - 1] != np.inf:
                return x1, y1, x2, y2

        if not(0 <= y1 < len(maze) and 0 <= x1 + 1 < len(maze[0])) or maze[y1][x1 + 1] == np.inf:
            if y1 < y2 and 0 <= y1 + 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1 + 1][x1] != np.inf:
                x1, y1, x2, y2 = move_up(path, maze, (x1, y1), (x2, y2), "R")
                continue
            elif y1 >= y2 and 0 <= y1 - 1 < len(maze) and 0 <= x1 < len(maze[0]) and maze[y1-1][x1] != np.inf:
                x1, y1, x2, y2 = move_down(path, maze, (x1, y1), (x2, y2), "R")
                continue
        x1 += 1
        print(x1, y1, "\t", x2, y2)
        path.append([(x1, y1), maze[y1][x1]])
    return x1,y1,x2,y2

def main():
    maze = [[0.0, 0.4, np.inf, 0.4, 0.4, 0.2],
            [0.1, 0.1, np.inf, 0.6, 0.6, 0.2],
            [np.inf, 0.0, np.inf, 0.8, 0.7, 0.5],
            [0.7, 0.8, np.inf, 0.9, 0.8, 0.6],
            [0.7, np.inf, 0.8, 0.8, np.inf, 0.7],
            [0.5, 0.6, 0.6, np.inf, 0.4, 0.0]]

    start = (0, 0)
    end = (1, 0)

    path = astar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()