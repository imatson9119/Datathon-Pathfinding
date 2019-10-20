import numpy as np

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


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    num_it = 0
    # Loop until you find the end
    while len(open_list) > 0:
        num_it+=1
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # print(current_node.h)
        # Found the goal
        #print('open list:', [i.position for i in open_list])
        #print('closed list:',[i.position for i in closed_list])
        # print(current_node.position, '=', end_node.position)
        if current_node.position == end_node.position or num_it > 30:
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
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
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
        # Loop through children
        for child in children:
            cont = False
            # Child is on the closed list
            for closed_child in closed_list:
                if child.position == closed_child.position:
                    cont = True
                    continue
            if cont:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + child.cost
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2))**(1/2) * current_node.cost
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    cont = True
                    continue
            if cont:
                continue
            # Add the child to the open list
            open_list.append(child)


def main():
    maze = [[0.0, 0.4, np.inf, 0.4, 0.4, 0.2],
            [0.1, 0.1, np.inf, 0.6, 0.6, 0.2],
            [np.inf, 0.0, np.inf, 0.8, 0.7, 0.5],
            [0.7, 0.8, np.inf, 0.9, 0.8, 0.6],
            [0.7, np.inf, 0.8, 0.8, np.inf, 0.7],
            [0.5, 0.6, 0.6, np.inf, 0.4, 0.0]]

    start = (0, 0)
    end = (5, 5)

    path = astar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()