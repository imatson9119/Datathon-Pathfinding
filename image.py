import cv2
import numpy as np

def makeRed(img):
    r = np.stack((img,) * 3, axis=-1)
    r[:, :, 1] = r[:, :, 1]-255
    r[:, :, 2] = r[:, :, 2]-255
    return r

def colorPath(img, path):
    c = img.copy()
    for p in path:
        pair = p[0]
        for i in range(-2,3):
            for j in range(-2,3):
                c[pair[1]+i][pair[0]+j][0] = 0
                c[pair[1]+i][pair[0]+j][1] = 255
    return c