import numpy as np
import math as math

def getRow(i, numOfRows):
    return (i % numOfRows) +1


def getCol(i, numOfRows):
    return math.floor(i / numOfRows) +1


def checkpixels_4(dayImage, nightImage, dicti, numOfRows):
    for i in range(dayImage.shape[0]):

        colCount = int(getCol(i, numOfRows))
        rowCount = int(getRow(i, numOfRows))
        if nightImage[i, 1] == 0 or dayImage[i, 1] == 0 or np.isnan(nightImage[i, 1]) or np.isnan(dayImage[i, 1]):
            continue
        counter = 0
        # run on the bands, start from the second band in order to compare to the previous one and calc M
        for k in range((dayImage.shape[1]-1)):
            dayValue1 = dayImage[i, (k + 1)]
            dayValue2 = dayImage[i, k]
            nightValue1 = nightImage[i, k + 1]
            nightValue2 = nightImage[i, k]
            mDay = (dayValue1 - dayValue2) / ((k + 1) - k)
            mNight = (nightValue1 - nightValue2) / ((k + 1) - k)
            if (mDay > 0 > mNight) or (mDay < 0 < mNight):
                counter += 1
        specdev = (1.0 * counter / (dayImage.shape[1]-1))
        if specdev > 0.7:
            keyInsert = '{0:.2f}'.format((specdev * 100) / 100)
            dicti.setdefault(keyInsert, []).extend((rowCount, colCount))