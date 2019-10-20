import numpy as np

def approx_distances(maze, target_x, target_y):
    penalty = 0
    slope=0
    adj = {}
    for i in range(len(target_x)):
        adj[i] = []

    for i in range(len(target_x)):
        x1 = target_x[i]
        y1 = target_y[i]
        for j in range(len(target_x)):
            x2 = target_x[j]
            y2 = target_y[j]

            dist = ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)
            adj[i].append((j, dist))
            if x2 - x1 != 0:
                slope = (y2-y1)//(x2-x1)
            print(slope)

    for key in adj.keys():
        print(key, adj[key])
