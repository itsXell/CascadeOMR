import cv2
import numpy as np
from copy import deepcopy
from HelperFunction import displayText

font = cv2.FONT_HERSHEY_COMPLEX


def Text(img, text, x, y):
    cv2.putText(img, text, (x, y - 5), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)


def scoreStack(stacks, sheet, flat, sharp, width, width_resize, height,
               height_resize, space, averageLocation, halfSpace, trebles,
               basses):
    flat = np.array(flat).tolist()
    sharp = np.array(sharp).tolist()
    for stack in stacks:
        score = ''
        locX = int(stack[0][0] * width / width_resize)
        locY = int(stack[0][1] * height / height_resize)
        for (x, y, w, h) in stack:
            x1 = x * width / width_resize
            y1 = y * height / height_resize
            x1 = int(round(x1))
            y1 = int(round(y1))
            isTreble, score = TrebleScore(trebles, flat, sharp, x1, y1, space,
                                          averageLocation, halfSpace, sheet,
                                          width, width_resize, height,
                                          height_resize, score)
            if not isTreble:
                score = BassScore(basses, flat, sharp, x1, y1, space,
                                  averageLocation, halfSpace, sheet, width,
                                  width_resize, height, height_resize, score)
        score = score[0:len(score) - 1]
        displayText(sheet, score, locX, locY)


def BassScore(basses, flats, sharps, x1, y1, space, averageLocation, halfSpace,
              sheet, width, width_resize, height, height_resize, score):
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
                            score += 'G#'
                            isCheck = True
                            break
                        else:
                            score += 'G' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 1:
                        if bass[0][1] > 5:
                            score += 'E#,'
                            isCheck = True
                            break
                        if bass[0][0] > 1:
                            score += 'Eb,'
                            isCheck = True
                            break
                        else:
                            score += 'E' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 2:
                        if bass[0][1] > 1:
                            score += 'C#,'
                            isCheck = True
                            break
                        if bass[0][0] > 5:
                            score += 'Cb,'
                            isCheck = True
                            break
                        else:
                            score += 'C' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 3:
                        if bass[0][1] > 4:
                            score += 'A#,'
                            isCheck = True
                            break
                        if bass[0][0] > 2:
                            score += 'Ab,'
                            isCheck = True
                            break
                        else:
                            score += 'A' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 4:
                        if bass[0][0] > 6:
                            score += 'Fb,'
                            isCheck = True
                            break
                        else:
                            score += 'F' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            break
                elif bass[1][i] + halfSpace - averageLocation <= y1 <= bass[1][
                        i] + halfSpace + averageLocation:
                    if i == 0:
                        if bass[0][1] > 0:
                            score += 'F#,'
                            isCheck = True
                            break
                        else:
                            score += 'F' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 1:
                        if bass[0][1] > 3:
                            score += 'D#,'
                            isCheck = True
                            break
                        if bass[0][0] > 3:
                            score += 'Db,'
                            isCheck = True
                            break
                        else:
                            score += 'D' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 2:
                        if bass[0][1] > 6:
                            score += 'B#,'
                            isCheck = True
                            break
                        if bass[0][0] > 0:
                            score += 'Bb, '
                            isCheck = True
                            break
                        else:
                            score += 'B' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 3:
                        if bass[0][0] > 4:
                            score += 'Gb,'
                            break
                        else:
                            score += 'G' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            break
                    if i == 4:
                        score += 'E' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        break
                elif bass[1][i] - halfSpace - averageLocation <= y1 <= bass[1][
                        i] - halfSpace + averageLocation:
                    if i == 0:
                        score += 'A' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        break
                elif bass[1][i] - (halfSpace + space
                                   ) - averageLocation <= y1 <= bass[1][i] - (
                                       halfSpace + space) + averageLocation:
                    if i == 0:
                        score += 'C' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] - space - averageLocation - 1 <= y1 <= bass[1][
                        i] - space + averageLocation:
                    if i == 0:
                        score += 'B' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        break
                elif bass[1][i] - (space *
                                   2) - averageLocation <= y1 <= bass[1][i] - (
                                       space * 2) + averageLocation:
                    if i == 0:
                        score += 'D' + sharpSymbol + flatSymbol + ','
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
                        score += 'F' + sharpSymbol + flatSymbol + ', '
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
                        score += 'A' + sharpSymbol + flatSymbol + ','
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
                        score += 'E' + sharpSymbol + flatSymbol + ','
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
                        score += 'G' + sharpSymbol + flatSymbol + ','
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
                        score += 'B' + sharpSymbol + flatSymbol + ','
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
                        score += 'D' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] + halfSpace - averageLocation <= y1 <= bass[1][
                        i] + halfSpace + averageLocation:
                    if i == 4:
                        score += 'E' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif bass[1][i] + space - averageLocation <= y1 <= bass[1][
                        i] + space + averageLocation:
                    if i == 4:
                        score += 'D' + sharpSymbol + flatSymbol + ','
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
                        score += 'C' + sharpSymbol + flatSymbol + ','
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
                        score += 'B' + sharpSymbol + flatSymbol + ', '
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
                        score += 'A' + sharpSymbol + flatSymbol + ','
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
                        score += 'G' + sharpSymbol + flatSymbol + ','
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
                        score += 'F' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
    return score


def TrebleScore(trebles, flats, sharps, x1, y1, space, averageLocation,
                halfSpace, sheet, width, width_resize, height, height_resize,
                score):
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
                            score += 'E#,'
                            isCheck = True
                            break
                        elif treble[0][0] > 1:
                            score += 'Eb,'
                            isCheck = True
                            break
                        else:
                            score += 'E' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 1:
                        if treble[0][1] > 1:
                            score += 'C#,'
                            isCheck = True
                            break
                        elif treble[0][0] > 5:
                            score += 'Cb,'
                            isCheck = True
                            break
                        else:
                            score += 'C' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 2:
                        if treble[0][1] > 4:
                            score += 'A#,'
                            isCheck = True
                            break
                        elif treble[0][0] > 2:
                            score += 'Ab,'
                            isCheck = True
                            break
                        else:
                            score += 'A' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 3:
                        score += 'F' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                    if i == 4:
                        score += 'D' + sharpSymbol + flatSymbol + ','
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
                            score += 'D#,'
                            isCheck = True
                            break
                        elif treble[0][0] > 3:
                            score += 'Db,'
                            isCheck = True
                            break
                        else:
                            score += 'D' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 1:
                        if treble[0][1] > 5:
                            score += 'B#,'
                            isCheck = True
                            break
                        elif treble[0][0] > 0:
                            score += 'Bb,'
                            isCheck = True
                        else:
                            score += 'B' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 2:
                        if treble[0][0] > 4:
                            score += 'Gb,'
                            isCheck = True
                            break
                        else:
                            score += 'G' + sharpSymbol + flatSymbol + ','
                            if currentSharp in sharps:
                                sharps.remove(currentSharp)
                            if currentFlat in flats:
                                flats.remove(currentFlat)
                            isCheck = True
                            break
                    if i == 3:
                        score += 'E' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                    if i == 4:
                        score += 'C' + sharpSymbol + flatSymbol + ','
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
                            score += 'F#,'
                            isCheck = True
                            break
                        else:
                            score += 'F' + sharpSymbol + flatSymbol + ','
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
                        score += 'A' + sharpSymbol + flatSymbol + ','
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
                            score += 'G#,'
                            isCheck = True
                            break
                        else:
                            score += 'G' + sharpSymbol + flatSymbol + ','
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
                        score += 'B' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break
                elif treble[1][i] + space - averageLocation <= y1 <= treble[1][
                        i] + space + averageLocation:
                    if i == 4:
                        score += 'B' + sharpSymbol + flatSymbol + ','
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
                        score += 'A' + sharpSymbol + flatSymbol + ','
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
                        score += 'G' + sharpSymbol + flatSymbol + ','
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
                        score += 'F' + sharpSymbol + flatSymbol + ','
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
                        score += 'E' + sharpSymbol + flatSymbol + ','
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
                        score += 'F' + sharpSymbol + flatSymbol + ','
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
                        score += 'D' + sharpSymbol + flatSymbol + ','
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
                        score += 'F' + sharpSymbol + flatSymbol + ','
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
                        score += 'C' + sharpSymbol + flatSymbol + ','
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
                        score += 'E' + sharpSymbol + flatSymbol + ','
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
                        score += 'G' + sharpSymbol + flatSymbol + ','
                        if currentSharp in sharps:
                            sharps.remove(currentSharp)
                        if currentFlat in flats:
                            flats.remove(currentFlat)
                        isCheck = True
                        break

        elif isCheck:
            break
    return isCheck, score


def groupUpNote(note):
    note = sorted(note, key=lambda x: x[1])
    note = np.array(note).tolist()
    cloneNote = deepcopy(note)
    stacks = []
    results = []
    check = 0
    if len(note) > 2:
        while (check >= 0):
            current = note[check]
            for i in range(len(note)):
                if current != note[i] and current[0] - 5 < note[i][
                        0] < current[0] + 5 and current[1] < note[i][
                            1] < current[1] + current[3]:
                    stacks.append(note[i])
                    if current not in stacks:
                        stacks.append(current)
                    if current in cloneNote:
                        cloneNote.remove(current)
                    if note[i] in cloneNote:
                        cloneNote.remove(note[i])
                elif note[i][1] > current[1] + 100:
                    break
            check += 1
            if check == len(note) - 1:
                check = -1
        stacks = sorted(stacks, key=lambda x: x[1])
        results = []
        for stack in stacks:
            check = False
            if len(results) == 0 and len(stacks) != 0:
                temp = []
                temp.append(stacks[0])
                results.append(temp)
            else:
                for result in results:
                    for subResult in result:
                        if subResult == stack:
                            check = True
                            break
                        elif subResult[0] - 10 < stack[0] < subResult[
                                0] + 10 and subResult[1] < stack[
                                    1] < subResult[1] + subResult[3]:
                            result.append(stack)
                            check = True
                if not check:
                    temp = []
                    temp.append(stack)
                    results.append(temp)
    return cloneNote, results