import numpy as np
from collections import deque


def findAllComponents(list, threshholdval, pollspread):
    blob = np.zeros_like(list)
    blobID = 1
    res = []
    for i in range(1, list.shape[0]-1, pollspread):
        for j in range(1, list.shape[1]-1, pollspread):
            if blob[i, j] == 0 and list[i, j] > threshholdval:
                bloblist = findNeighboursIteratively((i, j), list, blob, blobID, threshholdval)
                # blobID += 1
                res.append(bloblist)
    return res


def findComponent(origin, list, threshholdval):
    blob = np.zeros_like(list)
    blobID = 1
    return findNeighboursIteratively(origin, list, blob, blobID,threshholdval)


def findNeighboursIteratively(origin, list, blob, id, threshhold):
    indexQueue = deque(maxlen=(list.shape[0]*list.shape[1]))
    indexQueue.append(origin)
    blob[origin] = id
    size = 1
    res = np.zeros(list.shape, dtype=np.uint8)
    res[origin] = list[origin]
    max = (list.shape[0]-1, list.shape[1]-1)
    min = (1, 1)
    while indexQueue:
        center = indexQueue.pop()
        # Neighbour naming follows a 3x3 grid around the center pixel
        # 225  270  315
        # 180   C   000
        # 135  090  045

        ang000 = (center[0], center[1] + 1)
        ang045 = (center[0] + 1, center[1] + 1)
        ang090 = (center[0] + 1, center[1])
        ang135 = (center[0] + 1, center[1] - 1)
        ang180 = (center[0], center[1] - 1)
        ang225 = (center[0] - 1, center[1] - 1)
        ang270 = (center[0] - 1, center[1])
        ang315 = (center[0] - 1, center[1] + 1)
        if min[0] < center[0] < max[0] and min[1] < center[1] < max[1]:  # if current center i or j is within bounds
            origin_low = list[origin] - threshhold
            origin_high = list[origin] + threshhold
            if blob[ang000] == 0:  # if ang000 isn't traversed yet
                if origin_low < list[ang000] < origin_high :  # if the center value is within a certain threshhold
                    blob[ang000] = id
                    res[ang000] = list[ang000]
                    indexQueue.append(ang000)
            if blob[ang045] == 0:  # if ang000 isn't traversed yet
                if origin_low < list[ang045] < origin_high:  # if the center value is within a certain threshhold
                    blob[ang045] = id
                    res[ang045] = list[ang045]
                    indexQueue.append(ang045)
            if blob[ang090] == 0:  # if ang090 isn't traversed yet
                if origin_low < list[ang090] < origin_high:  # if the center value is within a certain threshhold
                    blob[ang090] = id
                    res[ang090] = list[ang090]
                    indexQueue.append(ang090)
            if blob[ang135] == 0:  # if ang090 isn't traversed yet
                if origin_low < list[ang135] < origin_high:  # if the center value is within a certain threshhold
                    blob[ang135] = id
                    res[ang135] = list[ang135]
                    indexQueue.append(ang135)
            if blob[ang180] == 0:  # if ang000 isn't traversed yet
                if origin_low < list[ang180] < origin_high:  # if the center value is within a certain threshhold
                    blob[ang180] = id
                    res[ang180] = list[ang180]
                    indexQueue.append(ang180)
            if blob[ang225] == 0: # if ang000 isn't traversed yet
                if origin_low < list[ang225] < origin_high:  # if the center value is within a certain threshhold
                    blob[ang225] = id
                    res[ang225] = list[ang225]
                    indexQueue.append(ang225)
            if blob[ang270] == 0:  # if ang000 isn't traversed yet
                if origin_low < list[ang270] < origin_high:  # if the center value is within a certain threshhold
                    blob[ang270] = id
                    res[ang270] = list[ang270]
                    indexQueue.append(ang270)
            if blob[ang315] == 0:  # if ang000 isn't traversed yet
                if origin_low < list[ang315] < origin_high:  # if the center value is within a certain threshhold
                    blob[ang315] = id
                    res[ang315] = list[ang315]
                    indexQueue.append(ang315)
    return res
