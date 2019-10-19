from walmartFunctions import *
import cv2
# Hyper parameters

image_map_source_filename = '1150.png' # The store map file location
target_seed = 42 # For determining the random target locations
noise_seed = 42 # For determining the random traffic noise locations

N_targets = 50 # The number of targets to be generated
circle_draw_size = 20 # Radius of targets to draw on goal image

# Prepare map

im_gray = cv2.imread('1150.png', cv2.IMREAD_GRAYSCALE)
display_img(im_gray)

thresh, im_bw = cv2.threshold(im_gray, 254, 255, cv2.THRESH_BINARY_INV)
display_img(im_bw, title="Store Map Collision")

#Make contour map

print(im_bw.shape)

collision_map = im_bw.copy()
contour = cv2.findContours(collision_map, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
print(contour)
for cnt in contour:
    cv2.drawContours(collision_map, [cnt], 0, 255, -1)
display_img(collision_map, title="Collision Map")
