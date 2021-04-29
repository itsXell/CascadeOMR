import cv2
import numpy as np
from copy import deepcopy


def removeDuplicateSharp(sharps):
    coordinates = np.array(sharps).tolist()
    clone = deepcopy(coordinates)
    for sharp in coordinates:
        x = sharp[0]
        y = sharp[1]
        w = sharp[2]
        h = sharp[3]
        if sharp in clone:
            for current in coordinates:
                cx = current[0]
                cy = current[1]
                cw = current[2]
                ch = current[3]
                if cy < y and (cy + h) > y and cx - 5 < x < cx + 5:
                    if current in clone:
                        clone.remove(current)
                        break
                    else:
                        break
                if y + 100 < cy:
                    break
    return clone