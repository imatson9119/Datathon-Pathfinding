import numpy as np
import cv2

def compressImage(img, factor):
    width = int(img.shape[1]/factor)
    height = int(img.shape[0]/factor)
    dims = (width, height)
    imgCompressed = cv2.resize(img, dims, interpolation = cv2.INTER_AREA)

    return imgCompressed