from gdal import ogr
import os
import csv

def readShp(inShp):
    typeList = []
    typeLength = []

    driverShp = ogr.GetDriverByName('Esri shapefile')
    inDir, inFile = os.path.split(inShp)
    layerName = os.path.splitext(inFile)[0]
    in_ds = ogr.Open(inDir)

    if in_ds is None:
        print 'Error opening input shapefile folder'

    lyr = in_ds.GetLayerByName(layerName)
    nFeat = lyr.GetFeatureCount()

    for i in range(0, nFeat, 1):
        feat = lyr.GetFeature(i)
        convType = feat.GetField('CONV_TYPE')
        featLen = feat.GetField('Shape_Leng')

        if convType in typeList:
            index = typeList.index(convType)
            typeLength[index] += featLen
        else:
            typeList.append(convType)
            typeLength.append(featLen)

    typeList.append('Total')
    typeLength.append(sum(typeLength))

    return typeList, typeLength

def summarize(inShp, outCsv):
    rowLabels, rowValues = readShp(inShp)
    colLabels = ['ConvType', 'Length', 'Percent']

    file = open(outCsv, 'wb')
    writer = csv.writer(file)
    writer.writerow(colLabels)

    for i in range(0, len(rowLabels), 1):
        rowList = [rowLabels[i], rowValues[i], rowValues[i]/rowValues[-1]*100.0]
        writer.writerow(rowList)

    file.close()

#Test funcs
path = r'E:\etal\Projects\USA\Utah\RiparianCondition\ConversionType\RVCT_SG_BoxElder.shp'
csvPath = r'C:\Users\khafe\Desktop\rvct.csv'
summarize(path, csvPath)