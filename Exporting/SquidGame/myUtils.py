import numpy as np


def makeOffsetPoly(path, offset, outer_ccw=1):
    def normalizeVec(x, y):
        distance = np.sqrt(x * x + y * y)
        return x / distance, y / distance

    num_points = len(path)
    newPath = []
    for curr in range(num_points):
        prev = (curr + num_points - 1) % num_points
        next = (curr + 1) % num_points

        vnX = path[next][0] - path[curr][0]
        vnY = path[next][1] - path[curr][1]
        vnnX, vnnY = normalizeVec(vnX, vnY)
        nnnX = vnnY
        nnnY = -vnnX

        vpX = path[curr][0] - path[prev][0]
        vpY = path[curr][1] - path[prev][1]
        vpnX, vpnY = normalizeVec(vpX, vpY)
        npnX = vpnY * outer_ccw
        npnY = -vpnX * outer_ccw

        bisX = (nnnX + npnX) * outer_ccw
        bisY = (nnnY + npnY) * outer_ccw

        bisnX, bisnY = normalizeVec(bisX, bisY)
        bislen = offset / np.sqrt(1 + nnnX * npnX + nnnY * npnY)

        newPath.append([int(path[curr][0] + bislen * bisnX), int(path[curr][1] + bislen * bisnY)])

    return newPath


def isPointInLine(line, point):
    x1, y1 = line[0]
    x2, y2 = line[1]
    x, y = point
    if x1 == x2:
        if y1 > y2:
            if y2 < y < y1:
                return True
            else:
                return False
        else:
            if y1 < y < y2:
                return True
            else:
                return False
    else:
        m = (y2 - y1) / (x2 - x1)
        c = y2 - m * x2
        yNew1 = int(m * x + c)
        yNew2 = int(m * x + c)
        if yNew1 - 40 < y < yNew2 + 40:
            return True
        else:
            return False
