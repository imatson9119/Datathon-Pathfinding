import cv2
import numpy as np

def makeRed(img):
    r = np.stack((img,) * 3, axis=-1)
    r[:, :, 1] = r[:, :, 1]-255
    r[:, :, 2] = r[:, :, 2]-255
    return r

def colorPath(img, path):
    c = img.copy()
    for pair in path:
        c[pair[1]][pair[0]][0] = 0
        c[pair[1]][pair[0]][1] = 255