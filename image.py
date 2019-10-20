import opencv

def makeRed(img):
    r = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)
    r[:, :, 0] = 0
    r[:, :, 1] = 0
    return r

def colorPath(img, path):
    for pair in path:
        img[pair[1]][pair[0]][2] = 0
        img[pair[1]][pair[0]][1] = 255