import sys
import numpy as np
import cv2
from HelperFunction import *
from LineDetection import lineDetection
from StackingFunction import *
from Remover import *
import time
import imutils
from copy import deepcopy

# cascade & resize
note = cv2.CascadeClassifier('Models/quarter/note.xml')
treble = cv2.CascadeClassifier('Models/treble/treble.xml')
bass = cv2.CascadeClassifier('Models/base/base.xml')
sharp = cv2.CascadeClassifier('Models/sharp/sharp.xml')
flat = cv2.CascadeClassifier('Models/flat/flat.xml')
quat = cv2.CascadeClassifier('Models/quarter/fullNote.xml')
fullquat = cv2.CascadeClassifier('Models/quarter/fullQuat.xml')

# S group

img = cv2.imread('input/testing.png')
sheet = ""
notes = ""
quats = ""
fullquats = ""

flats = ""
sharps = ""

basses = ""
trebles = ""

height = ""
width = ""
height_resize = ""
width_resize = ""


def SetUp(imgAcc):
    global img, sheet, trebles, notes, flats, quats, basses, fullquats, sharps, height, height_resize, width, width_resize
    img = cv2.imread(imgAcc)
    h, w, c = img.shape
    if h > 2000:
        print("Resizing")
        img = imutils.resize(img, height=2000)
    height, width, c = img.shape
    resized = cv2.resize(img, (width + 2200, height + 2200))
    height_resize, width_resize, c = resized.shape
    before = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sheet = cv2.cvtColor(before, cv2.COLOR_GRAY2BGR)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    grayOrigin = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, otsu = cv2.threshold(grayOrigin, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    line_edge = cv2.Canny(sheet, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(line_edge, 1, np.pi / 180, 250)
    notes = note.detectMultiScale(gray, 1.20, 3)
    trebles = treble.detectMultiScale(gray, 1.20, 2)
    basses = bass.detectMultiScale(gray, 1.20, 2)
    sharps = sharp.detectMultiScale(gray, 1.20, 3)
    flats = flat.detectMultiScale(gray, 1.20, 2)
    quats = quat.detectMultiScale(gray, 1.20, 3)
    fullquats = fullquat.detectMultiScale(gray, 1.20, 2)


def Rectangle(notes, color1, color2, color3):
    for (x, y, w, h) in notes:
        x1 = x * width / width_resize
        y1 = y * height / height_resize
        w1 = w * height / height_resize
        h1 = h * height / height_resize
        cv2.rectangle(sheet, (int(x1), int(y1)),
                      (int(x1) + int(w1), int(y1) + int(h1)),
                      (color1, color2, color3), 1)


def GetTreble():
    global basses, flats, sharps, quats, fullquats, notes
    line = lineDetection(img)
    print("IN LINE")
    removeDup = removeDuplicate(line)
    print("Remove LINE")
    space = findSpace(removeDup)
    staffLine = createStaffline(removeDup, space)
    notes, stacks = groupUpNote(notes)
    quats, stacksQuat = groupUpNote(quats)
    # fullquats, stackFullQuat = groupUpNote(fullquats)
    sharps = countSharpsFlats(staffLine, basses, trebles, False, sharps, width,
                              width_resize, height, height_resize)
    sharps = np.array(sharps)
    flats = countSharpsFlats(staffLine, basses, trebles, True, flats, width,
                             width_resize, height, height_resize)
    flats = np.array(flats)
    BassLoc = getTrebleBassLoc(basses, staffLine, height, height_resize, width,
                               width_resize)
    TrebleLoc = getTrebleBassLoc(trebles, staffLine, height, height_resize,
                                 width, width_resize)
    BassTreble = updateTrebleAndBassLoc(TrebleLoc, BassLoc)
    #Rectangle(notes)
    #Rectangle(basses)
    TLoc = BassTreble[0]
    BLoc = BassTreble[1]
    space = 0
    for line in staffLine:
        if len(line[1]) > 2:
            space = line[1][1] - line[1][0]
            break
    halfSpace = np.floor(space / 2)
    averageLocation = np.floor(space * 0.25)
    print("HEY HERE !", len(notes) + len(quats) + len(fullquats))
    # Rectangle(quats, 0, 256, 0)  #green
    # Rectangle(fullquats, 256, 0, 0)  #red
    # Rectangle(flats, 0, 0, 256)  #blue
    # Rectangle(notes, 255, 128, 0)  #sky blue
    # Rectangle(trebles, 255, 51, 255)  #pink
    # Rectangle(basses, 255, 51, 153)  #purple
    # Rectangle(sharps, 0, 255, 255)  #yellow
    Score(sheet, flats, sharps, notes, width, width_resize, height,
          height_resize, space, averageLocation, halfSpace, TLoc, BLoc)
    Score(sheet, flats, sharps, quats, width, width_resize, height,
          height_resize, space, averageLocation, halfSpace, TLoc, BLoc)
    Score(sheet, flats, sharps, fullquats, width, width_resize, height,
          height_resize, space, averageLocation, halfSpace, TLoc, BLoc)
    scoreStack(stacks, sheet, flats, sharps, width, width_resize, height,
               height_resize, space, averageLocation, halfSpace, TLoc, BLoc)
    scoreStack(stacksQuat, sheet, flats, sharps, width, width_resize, height,
               height_resize, space, averageLocation, halfSpace, TLoc, BLoc)
    # scoreStack(fullquats, sheet, flats, sharps, width, width_resize, height,
    #            height_resize, space, averageLocation, halfSpace, TLoc, BLoc)


#12.528131008148193 ( 2000 )
#26.933358192443848 ( 3500 )


def NoteRecognize(img):
    start_time = time.time()
    print('Start Detecting', img)
    SetUp(img)
    print("After set up")
    GetTreble()
    print("Finish Detecting")
    print("--- %s seconds ---" % (time.time() - start_time))
    return sheet

# print( NoteRecognize('./static/img/sheets/C/Easy/Away In a Manager.jpg'))