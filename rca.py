from gdal import ogr
import os
import csv

def conditionList():
    cond = [None]*5
    cond[0] = 'poor'
    cond[1] = 'moderate'
    cond[2] = 'good'
    cond[3] = 'intact'
    cond[4] = 'total'
    return cond

def maxRange():
    upper = [None]*4
    upper[0] = 0.4
    upper[1] = 0.65
    upper[2] = 0.85
    upper[3] = 1.0
    return upper

def minRange():
    lower = [None]*4
    lower[0] = 0.0
    lower[1] = 0.4
    lower[2] = 0.65
    lower[3] = 0.85
    return lower

def readShp(inPath):
    lengths = [0.0]*5
    driverShp = ogr.GetDriverByName('Esri shapefile')
    inDir, inFile = os.path.split(inPath)
    layerName = os.path.splitext(inFile)[0]
    in_ds = ogr.Open(inDir)

    if in_ds is None:
        print 'Error opening input shapefile folder'

    lyr = in_ds.GetLayerByName(layerName)
    nFeat = lyr.GetFeatureCount()
    upper = maxRange()

    for i in range(0, nFeat, 1):
        feat = lyr.GetFeature(i)
        condScore = feat.GetField('CONDITION')
        featLen = feat.GetField('Shape_Leng')
        if condScore >= 0.0 and condScore <= upper[0]:
            lengths[0] += featLen
        elif condScore > upper[0] and condScore <= upper[1]:
            lengths[1] += featLen
        elif condScore > upper[1] and condScore <= upper[2]:
            lengths[2] += featLen
        elif condScore > upper[2] and condScore <= upper[3]:
            lengths[3] += featLen
        else:
            print 'Condition score out of range ' + str(condScore)

    lengths[4] = sum(lengths)
    return lengths

def summarize(inPath, outPath):
    rowLabels = conditionList();
    rowValues = readShp(inPath);
    colLabels = ['Condition', 'Length', 'Percent']

    file = open(outPath, 'wb')
    writer = csv.writer(file)
    writer.writerow(colLabels)

    for i in range(0, len(rowLabels), 1):
        rowList = [rowLabels[i], rowValues[i], rowValues[i]/rowValues[-1]]
        writer.writerow(rowList)

    file.close()

#Test funcs
path = r'E:\etal\Projects\USA\Utah\RiparianCondition\ConditionAssessment\RCA_SageGrouse.shp'
csvPath = r'C:\Users\khafe\Desktop\rca_all.csv'
summarize(path, csvPath)
