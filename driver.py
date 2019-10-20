from walmartFunctions import *
from compress import *
from image import *
import cv2
import astar2 as astar
import approximateCost
import TravelingSalesman as tsp
import helpme
import SimAnnealing
# Hyper parameters

print("Input number of deals: ")
n = int(input())
print("Input noise seed:")
noise_seed = int(input())
print("Input target seed:")
target_seed = int(input())

travel_friction, target_points = get_traffic_map_and_targets(n, noise_seed, target_seed, scale_factor=5)
disp_img = travel_friction.copy()

target_xs = []
target_ys = []
for i in range(len(target_points)):
    target_xs.append(target_points[i][0])
    target_ys.append(target_points[i][1])

circle_draw_size = 5
for x, y in zip(target_xs, target_ys):
    cv2.circle(disp_img, (x, y), circle_draw_size, (0, 0, 0), -1)
#display_img(disp_img*255)

nodes = approximateCost.approx_distances(travel_friction, target_xs, target_ys)
points = []
#print("_________")
for i in range(len(target_xs)):
    points += [(target_xs[i], target_ys[i])]
#print(points)

# order, distance = tsp.greedyTravelingWithSwaps(nodes, 0)
# tsp.plotTSP([order], points)
sa = SimAnnealing.SimAnneal(points, stopping_iter=5000)
sa.anneal()
order = sa.best_solution

megaPath = []
totalCost = 0
print(target_xs)
print(target_ys)
for i in range(len(target_xs) - 1):
    print("Returning", i)
    start = (target_ys[order[i]], target_xs[order[i]])
    end = (target_ys[order[i+1]], target_xs[order[i+1]])
    #print("\n!_!_!_!_!_!")
    path, cost = astar.astar(travel_friction, start, end)
    megaPath += path
    totalCost = cost
print(megaPath)
red = makeRed(travel_friction)
# display_img(red)
drawn = colorPath(red,megaPath)
display_img(drawn)

print(totalCost)

megaPath = [megaPath[i][0] for i in range(len(megaPath))]
#print(megaPath)
print("Score:", evaluate_path(travel_friction, target_points, megaPath))



