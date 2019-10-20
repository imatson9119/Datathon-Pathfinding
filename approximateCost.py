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
            x1 = target_x[i]
            y1 = target_y[i]
            x2 = target_x[j]
            y2 = target_y[j]

            dist = ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)


            sample_points = []
            if x2 - x1 != 0 and (y2-y1 > 60 or x2-x1 > 60):
                rise, run = (y2-y1)//15, (x2-x1)//15
                x1 += run
                y1 += rise

                for k in range(15):
                    if(maze[y1][x1] != np.inf):
                        sample_points.append(maze[y1][x1])
                    x1 += run
                    y1 += rise
                if len(sample_points) >= 1:
                    average = sum(sample_points)/len(sample_points)
                    adj[i].append((j, average * dist))
                else:
                    adj[i].append((j, dist))
            else:
                adj[i].append((j, dist))
    for key in adj.keys():
        print(key, adj[key])
    return adj



