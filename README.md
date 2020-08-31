# Walmart Best Path - TAMU Datathon 2019
1st Place winner for Walmart Technology at TAMU Datathon 2019 - https://2019.tamudatathon.com/

# Challenge Description
Black Friday is coming, and Walmart has a lot of great deals for its customers. As a smart shopper, you will use computer to make a plan to visit the in-store deals as quick as possible.

## Input Data
- Store Map
- Location of deals
- Traffic heatmap

![Imgur Image](https://i.imgur.com/4ypYeQ0l.png)

## Objectives
- Make a model to generate the optimal travel plan
- Stretch goal: Create a simulation environment to visualize the model
- Stretch goal: Help store manager by providing a model to optimize the deals locations

# Solution
To solve this problem, we used the OpenCV library in Python. As input on the store map, we were given the coordinates of the deals on the image.

Originally, our idea was to use the A* path-finding algorithm to find paths from every deal to every other deal on the store map. We would then use these paths to solve the travelling salesman problem and determine the optimal order to visit the deals in. 

However, running the A* algorithm that many times turned out to take too long, so we decided to swap the order and solve the travelling salesman problem first. To do so, we first approximated all the distances by simply calculating the euclidean distance between all the points. Then, we built a graph with the euclidean distances as the edge weights.

To actually solve (approximate) the travelling salesman problem, we first used an "edge swapping" method. We would first build a random solution by selecting random edges on the graph. Then, we would randomly swap a bunch of the edges with each other, and if they yielded an improvement, we would allow the swap to be made. After some more investigation, we discovered a technique called "Simulated Annealing (SA)" that led to slightly better results, so we ended up using that. You can read more about SA here: https://en.wikipedia.org/wiki/Simulated_annealing. Here is an example solution to the travelling salesman problem that our algorithm came up with:

![Imgur Image](https://i.imgur.com/Lv6G5fu.jpg)

Finally, after finding the order that we needed to visit the deals in, we used the A* algorithm to construct a final path between all the deals. We tried incorporating the traffic heatmap into our heuristic function with limited success, and in the end, we decided to simply minimize distance in order to stay under the 60 second runtime limit.

Here is an example of a path generated by our algorithm:

![Imgur Image](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/000/867/206/datas/gallery.jpg)