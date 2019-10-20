from walmartFunctions import *
from compress import *
import cv2
import astar
import approximateCost
# Hyper parameters

image_map_source_filename = '1150.png' # The store map file location
target_seed = 42 # For determining the random target locations
noise_seed = 42 # For determining the random traffic noise locations

N_targets = 50 # The number of targets to be generated
circle_draw_size = 20 # Radius of targets to draw on goal image

# Prepare map

im_gray = cv2.imread('1150.png', cv2.IMREAD_GRAYSCALE)
#display_img(im_gray)

#im_gray = compressImage(im_gray,4)
#display_img(im_gray)

thresh, im_bw = cv2.threshold(im_gray, 254, 255, cv2.THRESH_BINARY_INV)
#display_img(im_bw, title="Store Map Collision")

#Make contour map

print(im_bw.shape)

collision_map = im_bw.copy()
contour, hier = cv2.findContours(collision_map, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contour:
    cv2.drawContours(collision_map, [cnt], 0, 255, -1)
#display_img(collision_map, title="Collision Map")
#print(collision_map)

# Targets
valid_targets = cv2.Laplacian(collision_map, cv2.CV_64F)
#display_img(valid_targets, title="Possible Targets Map")

random.seed(target_seed)
im_targets = im_gray.copy()
ys, xs = valid_targets.nonzero()
target_indicies = random.sample(range(len(xs)), N_targets)
target_xs, target_ys = xs[target_indicies], ys[target_indicies]
for x, y in zip(target_xs, target_ys):
    cv2.circle(im_targets, (x, y), circle_draw_size, (0, 255, 0), -1)
#display_img(im_targets)


# Add traffic map
width, height = len(im_targets[0]), len(im_targets)
noise_img = generate_noise_image(width, height, seed=noise_seed)
noise_img = (noise_img - np.min(noise_img)) / (np.max(noise_img) - np.min(noise_img))

travel_friction = (~collision_map>0).astype(int) * noise_img
travel_friction[collision_map>0] = np.inf
for x, y in zip(target_xs, target_ys):
    travel_friction[y][x] = 0

display_img(travel_friction*255)
print(travel_friction)
lines = []
for i in travel_friction:
    lines.append(max(i))
    if np.inf in i:
        print("Found infinity")
print(max(i))
print(target_xs)
print(target_ys)

approximateCost.approx_distances(travel_friction, target_xs, target_ys)