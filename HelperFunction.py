import cv2
import numpy as np
from copy import deepcopy


def Retangle(img, notes, width, height, resizedWidth, resizeHeight):
    for (x, y, w, h) in notes:
        x1 = x * width / resizedWidth
        y1 = y * height / resizeHeight
        w1 = w * height / resizeHeight
        h1 = h * height / resizeHeight
        new_img = cv2.rectangle(img, (int(x1), int(y1)),
                                (int(x1) + int(w1), int(y1) + int(h1)),
                                (255, 0, 0), 1)
        return new_img


def getTrebleBassLoc(coordinate, staffLines, height, height_resize, width,
                     width_resize):
    seen = set()
    BassLocation = []
    newStaffLine = deepcopy(staffLines)
    for x, y, w, h in coordinate:
        y1 = np.floor(y * height / height_resize)
        w = np.floor(w * height / height_resize)
        y2 = np.floor(y1 + w)
        x = np.floor(x * width / width_resize)
        for staffLine in newStaffLine:
            t = tuple(staffLine[1])
            if t not in seen:
                if t not in seen:
                    first = staffLine[1][0]
                    last = staffLine[1][len(staffLine[1]) - 1]
                    # c = (y1 >= staffLine[1][0] and y2 <= staffLine[1][len(staffLine) - 1])
                    # d = (y1 <= staffLine[1][0] and y2 <= staffLine[1][len(staffLine) - 1])
                    if (y1 >= first and y2 <= last) or (
                            y1 <= first and y2 <= last
                            and y2 > first) or (y1 >= first and y2 > first
                                                and y2 < last + 20):
                        staffLine[0][2] = x
                        staffLine[0][3] = width
                        staffLine[0][4] = x + w
                        BassLocation.append(staffLine)
                        seen.add(t)
                        break
    return BassLocation


font = cv2.FONT_HERSHEY_COMPLEX


def displayText(img, text, x, y):
    # print(cv2.getTextSize(font))
    cv2.putText(img, text, (x, y - 5), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)


def updateTrebleAndBassLoc(trebles, basses):
    for treble in trebles:
        for bass in basses:
            if treble[1][0] == bass[1][0]:
                if treble[0][2] > bass[0][2]:
                    bass[0][3] = treble[0][2] - 20
                    break
                elif treble[0][2] < bass[0][2]:
                    treble[0][3] = bass[0][2] - 20
                    break
    return trebles, basses


def Score(sheet, flat, sharp, notes, width, width_resize, height,
          height_resize, space, averageLocation, halfSpace, trebles, basses):
    flat = np.array(flat).tolist()
    sharp = np.array(sharp).tolist()
    for (x, y, w, h) in notes:
        x1 = x * width / width_resize
        y1 = y * height / height_resize
        x1 = int(round(x1))
        y1 = int(round(y1))
        isTreble = TrebleScore(trebles, flat, sharp, x1, y1, space,
                               averageLocation, halfSpace, sheet, width,
                               width_resize, height, height_resize)
        if not isTreble:
            BassScore(basses, flat, sharp, x1, y1, space, averageLocation,
                      halfSpace, sheet, width, width_resize, height,
                      height_resize)


def BassScore(basses, flats, sharps, x1, y1, space, averageLocation, halfSpace,
              sheet, width, width_resize, height, height_resize):

    for bass in basses:
        if (x1 > bass[0][2]) and (x1 < bass[0][3]) and (
                bass[1][0] - (space * 5) +
            (averageLocation * 2) <= y1 <= bass[1][len(bass[1]) - 1] +
            (space * 5)) + (averageLocation * 2) and x1 > bass[0][4]:
            for i in range(0, len(bass[1])):
                sharpSymbol = ''
                flatSymbol = ''
                checkSharp = False
                currentSharp = []
                currentFlat = []
                if len(sharps) != 0:
                    for sharp in sharps:
                        sharpX = sharp[0] * width / width_resize
                        sharpY = sharp[1] * height / height_resize
                        w = sharp[2] * width / width_resize
                        h = sharp[3] * height / height_resize
                        sharpX = int(round(sharpX))
                        sharpY = int(round(sharpY))
                        # print(sharpX < x1 < (sharpX + (w + 20)) and sharpY - 10 < y1 < sharpY + h)
                        if sharpX < x1 < (
                                sharpX +
                            (w + 20)) and sharpY - 10 < y1 < sharpY + h:
                            sharpSymbol = '#'
                            currentSharp = sharp
                            checkSharp = True
                            break
                if len(flats) != 0 and not checkSharp:
                    for flat in flats:
                        flatX = flat[0] * width / width_resize
                        flatY = flat[1] * height / height_resize
                        w = flat[2] * width / width_resize
                        h = flat[3] * height / height_resize
                        flatX = int(round(flatX))
                        flatY = int(round(flatY))
                        if flatX < x1 < (
                                flatX + (w + 20)
                        ) and flatY - 10 < y1 < flatY + h and flat in flats:
                            flatSymbol = 'b'
                            currentFlat = flat
                            break

                if bass[1][i] - averageLocation <= y1 <= bass[1][
                        i] + averageLocation:
                    if i == 0:
                        if bass[0][1] > 2:
                            displayText(sheet, 'G#', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'G' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 1:
                        if bass[0][1] > 5:
                            displayText(sheet, 'E#', x1, y1)
                            isCheck = True
                            break
                        if bass[0][0] > 1:
                            displayText(sheet, 'Eb', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'E' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 2:
                        if bass[0][1] > 1:
                            displayText(sheet, 'C#', x1, y1)
                            isCheck = True
                            break
                        if bass[0][0] > 5:
                            displayText(sheet, 'Cb', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'C' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 3:
                        if bass[0][1] > 4:
                            displayText(sheet, 'A#', x1, y1)
                            isCheck = True
                            break
                        if bass[0][0] > 2:
                            displayText(sheet, 'Ab', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'A' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 4:
                        if bass[0][0] > 6:
                            displayText(sheet, 'Fb', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'F' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            break
                elif bass[1][i] + halfSpace - averageLocation <= y1 <= bass[1][
                        i] + halfSpace + averageLocation:
                    if i == 0:
                        if bass[0][1] > 0:
                            displayText(sheet, 'F#', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'F' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 1:
                        if bass[0][1] > 3:
                            displayText(sheet, 'D#', x1, y1)
                            isCheck = True
                            break
                        if bass[0][0] > 3:
                            displayText(sheet, 'Db', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'D' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 2:
                        if bass[0][1] > 6:
                            displayText(sheet, 'B#', x1, y1 - 3)
                            isCheck = True
                            break
                        if bass[0][0] > 0:
                            displayText(sheet, 'Bb', x1, y1 - 3)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'B' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 3:
                        if bass[0][0] > 4:
                            displayText(sheet, 'Gb', x1, y1 - 3)
                            break
                        else:
                            displayText(sheet, 'G' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            break
                    if i == 4:
                        displayText(sheet, 'E' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        break
                elif bass[1][i] - halfSpace - averageLocation <= y1 <= bass[1][
                        i] - halfSpace + averageLocation:
                    if i == 0:
                        displayText(sheet, 'A' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        break
                elif bass[1][i] - (halfSpace + space
                                   ) - averageLocation <= y1 <= bass[1][i] - (
                                       halfSpace + space) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'C' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] - space - averageLocation - 1 <= y1 <= bass[1][
                        i] - space + averageLocation:
                    if i == 0:
                        displayText(sheet, 'B' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        break
                elif bass[1][i] - (space *
                                   2) - averageLocation <= y1 <= bass[1][i] - (
                                       space * 2) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'D' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] - (space *
                                   3) - averageLocation <= y1 <= bass[1][i] - (
                                       space * 3) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'F' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] - (space *
                                   4) - averageLocation <= y1 <= bass[1][i] - (
                                       space * 4) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'A' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] - (
                        halfSpace +
                    (space * 2)) - averageLocation <= y1 <= bass[1][i] - (
                        halfSpace + (space * 2)) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'E' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] - (
                        halfSpace +
                    (space * 3)) - averageLocation <= y1 <= bass[1][i] - (
                        halfSpace + (space * 3)) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'G' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] - (
                        halfSpace +
                    (space * 4)) - averageLocation <= y1 <= bass[1][i] - (
                        halfSpace + (space * 4)) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'B' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] - (
                        halfSpace +
                    (space * 5)) - averageLocation <= y1 <= bass[1][i] - (
                        halfSpace + (space * 5)) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'D' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] + halfSpace - averageLocation <= y1 <= bass[1][
                        i] + halfSpace + averageLocation:
                    if i == 4:
                        displayText(sheet, 'E' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] + space - averageLocation <= y1 <= bass[1][
                        i] + space + averageLocation:
                    if i == 4:
                        displayText(sheet, 'D' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][
                        i] + space + halfSpace - averageLocation <= y1 <= bass[
                            1][i] + space + halfSpace + averageLocation:
                    if i == 4:
                        displayText(sheet, 'C' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] + (space *
                                   2) - averageLocation <= y1 <= bass[1][i] + (
                                       space * 2) + averageLocation:
                    if i == 4:
                        displayText(sheet, 'B' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] + (
                        space * 2) + halfSpace - averageLocation <= y1 <= bass[
                            1][i] + (space * 2) + halfSpace + averageLocation:
                    if i == 4:
                        displayText(sheet, 'A' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] + (space *
                                   3) - averageLocation <= y1 <= bass[1][i] + (
                                       space * 3) + averageLocation:
                    if i == 4:
                        displayText(sheet, 'G' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] + (
                        space * 3) + halfSpace - averageLocation <= y1 <= bass[
                            1][i] + (space * 3) + halfSpace + averageLocation:
                    if i == 4:
                        displayText(sheet, 'F' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break


def TrebleScore(trebles, flats, sharps, x1, y1, space, averageLocation,
                halfSpace, sheet, width, width_resize, height, height_resize):
    isCheck = False
    # print(sharps)

    for treble in trebles:
        if (x1 > treble[0][2]) and (x1 < treble[0][3]) and treble[1][0] - (
                space * 5) <= y1 <= treble[1][len(treble[1]) - 1] + (
                    space * 5) and x1 > treble[0][4]:
            for i in range(0, len(treble[1])):
                sharpSymbol = ''
                flatSymbol = ''
                currentSharp = []
                currentFlat = []
                checkSharp = False
                if len(sharps) != 0:
                    for sharp in sharps:
                        sharpX = sharp[0] * width / width_resize
                        sharpY = sharp[1] * height / height_resize
                        w = sharp[2] * width / width_resize
                        h = sharp[3] * height / height_resize
                        sharpX = int(round(sharpX))
                        sharpY = int(round(sharpY))
                        if sharpX < x1 < (
                                sharpX + (w + 20)
                        ) and sharpY - 10 < y1 < sharpY + h and sharp in sharps:
                            sharpSymbol = '#'
                            currentSharp = sharp
                            checkSharp = True
                            break
                if len(flats) != 0 and not checkSharp:
                    for flat in flats:
                        flatX = flat[0] * width / width_resize
                        flatY = flat[1] * height / height_resize
                        w = flat[2] * width / width_resize
                        h = flat[3] * height / height_resize
                        flatX = int(round(flatX))
                        flatY = int(round(flatY))
                        if flatX < x1 < (
                                flatX + (w + 20)
                        ) and flatY - 10 < y1 < flatY + h and flat in flats:
                            flatSymbol = 'b'
                            currentFlat = flat
                            break

                if (treble[1][i] - averageLocation) <= y1 <= (treble[1][i] +
                                                              averageLocation):
                    if i == 0:
                        if treble[0][1] > 5:
                            displayText(sheet, 'E#', x1, y1)
                            isCheck = True
                            break
                        elif treble[0][0] > 1:
                            displayText(sheet, 'Eb', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'E' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 1:
                        if treble[0][1] > 1:
                            displayText(sheet, 'C#', x1, y1)
                            isCheck = True
                            break
                        elif treble[0][0] > 5:
                            displayText(sheet, 'Cb', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'C' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 2:
                        if treble[0][1] > 4:
                            displayText(sheet, 'A#', x1, y1)
                            isCheck = True
                            break
                        elif treble[0][0] > 2:
                            displayText(sheet, 'Ab', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'A' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 3:
                        displayText(sheet, 'F' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                    if i == 4:
                        displayText(sheet, 'D' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] + halfSpace - averageLocation <= y1 <= treble[
                        1][i] + halfSpace + averageLocation:
                    if i == 0:
                        if treble[0][1] > 3:
                            displayText(sheet, 'D#', x1, y1)
                            isCheck = True
                            break
                        elif treble[0][0] > 3:
                            displayText(sheet, 'Db', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'D' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 1:
                        if treble[0][1] > 5:
                            displayText(sheet, 'B#', x1, y1)
                            isCheck = True
                            break
                        elif treble[0][0] > 0:
                            displayText(sheet, 'Bb', x1, y1)
                            isCheck = True
                        else:
                            displayText(sheet, 'B' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 2:
                        if treble[0][0] > 4:
                            displayText(sheet, 'Gb', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'G' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 3:
                        displayText(sheet, 'E' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                    if i == 4:
                        displayText(sheet, 'C' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break

                elif treble[1][i] - halfSpace - averageLocation <= y1 <= treble[
                        1][i] - halfSpace + averageLocation:
                    if i == 0:
                        if treble[0][1] > 0:
                            displayText(sheet, 'F#', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'F' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                elif treble[1][i] - (
                        halfSpace +
                        space) - averageLocation <= y1 <= treble[1][i] - (
                            halfSpace + space) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'A' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] - space - averageLocation <= y1 <= treble[1][
                        i] - space + averageLocation:
                    if i == 0:
                        if treble[0][1] > 2:
                            displayText(sheet, 'G#', x1, y1)
                            isCheck = True
                            break
                        else:
                            displayText(sheet, 'G' + sharpSymbol + flatSymbol,
                                        x1, y1)
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                elif treble[1][i] - (
                        space * 2) - averageLocation <= y1 <= treble[1][i] - (
                            space * 2) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'B' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] + space - averageLocation <= y1 <= treble[1][
                        i] + space + averageLocation:
                    if i == 4:
                        displayText(sheet, 'B' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][
                        i] + space + halfSpace - averageLocation <= y1 <= treble[
                            1][i] + space + halfSpace + averageLocation:
                    if i == 4:
                        displayText(sheet, 'A' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] + (
                        space * 2) - averageLocation <= y1 <= treble[1][i] + (
                            space * 2) + averageLocation:
                    if i == 4:
                        displayText(sheet, 'G' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] + (
                        space * 2
                ) + halfSpace - averageLocation <= y1 <= treble[1][i] + (
                        space * 2) + halfSpace + averageLocation:
                    if i == 4:
                        displayText(sheet, 'F' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] + (
                        space * 3) - averageLocation <= y1 <= treble[1][i] + (
                            space * 3) + averageLocation:
                    if i == 4:
                        displayText(sheet, 'E' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] + (
                        space * 3
                ) + halfSpace - averageLocation <= y1 <= treble[1][i] + (
                        space * 3) + halfSpace + averageLocation:
                    if i == 4:
                        displayText(sheet, 'F' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] - (
                        space * 3) - averageLocation <= y1 <= treble[1][i] - (
                            space * 3) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'D' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] - (
                        space * 4) - averageLocation <= y1 <= treble[1][i] - (
                            space * 4) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'F' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] - (
                        halfSpace +
                    (space * 2)) - averageLocation <= y1 <= treble[1][i] - (
                        halfSpace + (space * 2)) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'C' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] - (
                        halfSpace +
                    (space * 3)) - averageLocation <= y1 <= treble[1][i] - (
                        halfSpace + (space * 3)) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'E' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] - (
                        halfSpace +
                    (space * 4)) - averageLocation <= y1 <= treble[1][i] - (
                        halfSpace + (space * 3)) + averageLocation:
                    if i == 0:
                        displayText(sheet, 'G' + sharpSymbol + flatSymbol, x1,
                                    y1)
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break

        elif isCheck:
            break
    return isCheck


def countSharpsFlats(Staffline, Bass, Treble, isFlat, coordinates, width,
                     width_resize, height, height_resize):
    length = np.floor(width * 0.15)
    # coordinates = list(coordinates)
    coordinates = np.array(coordinates).tolist()
    clone = deepcopy(coordinates)
    for coordinate in coordinates:
        x1 = coordinate[0] * width / width_resize
        y1 = coordinate[1] * height / height_resize
        h1 = coordinate[3] * height / height_resize
        x1 = int(round(x1))
        y1 = int(round(y1))
        for line in Staffline:
            if line[1][0] - 50 <= y1 <= line[1][len(line[1]) - 1] + 20:
                for bass in Bass:
                    xb = bass[0] * width / width_resize
                    yb = bass[1] * height / height_resize
                    hb = bass[3] * height / height_resize
                    xb = int(round(xb))
                    yb = int(round(yb))
                    if yb - 20 <= y1 <= yb + hb + 20 and xb <= x1 <= xb + 100:
                        if coordinate in clone:
                            if isFlat:
                                clone.remove(coordinate)
                                line[0][0] += 1
                                break
                            else:
                                clone.remove(coordinate)
                                line[0][1] += 1
                                break
                for treble in Treble:
                    xt = treble[0] * width / width_resize
                    yt = treble[1] * height / height_resize
                    ht = treble[3] * height / height_resize
                    xt = int(round(xt))
                    yt = int(round(yt))
                    if yt - 20 <= y1 <= yt + ht + 20 and xt <= x1 <= xt + 100:
                        if coordinate in clone:
                            if isFlat:
                                clone.remove(coordinate)
                                line[0][0] += 1
                                break
                            else:
                                clone.remove(coordinate)
                                line[0][1] += 1
                                break
    return clone


def removeDuplicate(lines):
    singleLine = []
    current = 0
    for i in lines:
        if i - current > 5:
            current = i
            singleLine.append(i)
        else:
            pass
    return singleLine


def findSpace(singleLine):
    arrayLine = []
    space = 25
    current = singleLine[0]
    for line in singleLine:
        if line - current < 25:
            arrayLine.append(line)
            current = line
            if len(arrayLine) > 4:
                lengths = []
                for i in range(len(arrayLine) - 1):
                    if i < len(arrayLine):
                        length = arrayLine[i + 1] - arrayLine[i]
                        lengths.append(length)
                totalLength = sum(lengths)
                space = totalLength / len(arrayLine)
                space += 5
                break
        else:
            current = line
            arrayLine = []
    return space


def createStaffline(singleLine, space):
    staff_line = [[[], []]]
    index = 0
    current = singleLine[0]
    currentList = [[], []]
    staff_line[index][0] += 5 * [0]
    for line in singleLine:
        # staff_line[0] = 0
        if line - current < space:
            # staff_line[0] = 0
            staff_line[index][1].append(line)
            # if len(staff_line[index][1]) > 5:
            #     lengthLine = []
            #     for i  in range(len(staff_line[index][1])-1):
            #         if i < len(staff_line[index][1]):
            #             x = staff_line[index][1][i+1] - staff_line[index][1][i]
            #             lengthLine.append(x)
            #     totalLength = sum(lengthLine)
            # print(totalLength)
            current = line
        else:
            currentList = []
            value = []
            value += 5 * [0]
            index += 1
            Location = []
            Location.append(line)
            currentList.append(value)
            currentList.append(Location)
            staff_line.append(currentList)
            current = line

    return staff_line
