import cv2
import numpy as np
import math


def lineDetection(img):
    grays = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(grays)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, 15, -2)
    # cv2.imshow('gray', bw)
    horizontal = np.copy(bw)
    vertical = np.copy(bw)
    cols = horizontal.shape[1]
    horizontal_size = cols // 5
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                    (horizontal_size, 1))
    horizontal = cv2.erode(horizontal, horizontalStructure)
    # cv2.imshow('erode', horizontal)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    kernel_size = 5

    blur_gray = cv2.GaussianBlur(horizontal, (kernel_size, kernel_size), 0)
    edges = cv2.Canny(blur_gray, 50, 150)
    # cv2.imshow('erode', edges)
    lines = cv2.HoughLinesP(edges,
                            1,
                            np.pi / 180,
                            100,
                            minLineLength=100,
                            maxLineGap=250)
    lineLocation = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
        if angle == 0 or angle == 180:
            # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)
            lineLocation.append(y1)
    lineLocation.sort()
    return lineLocation
