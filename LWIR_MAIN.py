
#spectral is to read hyperspectral images
from spectral import *
import numpy as np
import checkpixels as check
import os
import pandas as pd


# select folder - create a sub-folder for the results
folder = r'D:\my tools\Desktop\python scripts\lwir'
os.chdir(folder)
path = 'AGStemp1'
new_directory = folder + '\\' + path
if not os.path.exists(new_directory):
    os.makedirs(new_directory)

# insert day and night names from directory - this reads the meta data without the values in each pixel
day_file = envi.open('RamonA_D_E_mosaic_subset.hdr', 'RamonA_D_E_mosaic_subset')
night_file = envi.open('RamonA_N_E_mosaic_subset.hdr', 'RamonA_N_E_mosaic_subset')

# get image dimensions
numOfRows, numOfLines, numOfBands = day_file.shape
totalPixelsInImage = numOfRows * numOfLines

# init vars
dicti = {}


# load the files, reshape them from 3 dimension to 2 dimension to 3 dimension by stacking columns
#  and calculate pixel variance with checkpixels func
dayImage = day_file.load().reshape((day_file.shape[0] * day_file.shape[1]), day_file.shape[2], order='F')
nightImage = night_file.load().reshape((night_file.shape[0] * night_file.shape[1]), night_file.shape[2], order='F')
check.checkpixels_4(dayImage, nightImage, dicti, numOfRows)

# a bunch of stuff to edit the output and
# save and export
vec = dicti.keys()
vec.sort()
tempVar3 = []
dict2 = {}
for element in range((len(vec) - 1), 1, -1):
    tempVar = dicti[vec[element - 1]]
    tempVar2 = dicti[vec[element]]
    tempVar.extend(tempVar2)
    dicti[vec[element - 1]] = tempVar
    numOfPixelsFound = len(dicti[vec[element]]) / 2
    percentOfPixelsFound = 1.0 * numOfPixelsFound / totalPixelsInImage
    thresh = vec[element]
    dict2[thresh] = [numOfPixelsFound, percentOfPixelsFound]
    # generate roi location file
    tempSaveName = str(vec[element])
    a = dicti[vec[element]]
    b = np.array(a[0:len(a) - 1:2])[np.newaxis]
    b = b.T
    c = np.array(a[1:len(a):2])[np.newaxis]
    c = c.T
    b = np.hstack((b, c))
    np.savetxt(new_directory + '\\' + tempSaveName + '.txt', b, fmt="%s")

# last cast
# generate ROI location file
tempSaveName = str(vec[0])
a = dicti[vec[0]]
b = np.array(a[0:len(a)-1:2])[np.newaxis]
b = b.T
c = np.array(a[1:len(a):2])[np.newaxis]
c = c.T
b = np.hstack((b,c))
np.savetxt(new_directory+'\\' + tempSaveName+'.txt', b, fmt="%s")

numOfPixelsFound = len(dicti[vec[0]]) / 2
percentOfPixelsFound = 1.0 * numOfPixelsFound / totalPixelsInImage
thresh = vec[0]
dict2[str(thresh)] = [numOfPixelsFound, percentOfPixelsFound]

# save algo results
df = pd.DataFrame.from_dict(dict2, orient='index')
writer = pd.ExcelWriter(new_directory+'\\' + 'output.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()

