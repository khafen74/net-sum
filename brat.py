from gdal import ogr
import os
import csv

def readShp(inShp):
    restList = []
    restLength = []
    capList = []
    exLength = []
    ptLength = []

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
        restType = feat.GetField('oPBRC')
        exType = feat.GetField('Ex_Categor')
        ptType = feat.GetField('Pt_Categor')
        featLen = feat.GetField('iGeo_Lengt')

        if restType in restList:
            restLength[restList.index(restType)] += featLen
        else:
            restList.append(restType)
            restLength.append(featLen)

        if exType in capList:
            exLength[capList.index(exType)] += featLen
        else:
            capList.append(exType)
            exLength.append(featLen)
            ptLength.append(0.0)

        if ptType in capList:
            ptLength[capList.index(ptType)] += featLen
        else:
            capList.append(exType)
            ptLength.append(featLen)
            exLength.append(0.0)

    restList.append('Total')
    restLength.append(sum(restLength))
    capList.append('Total')
    exLength.append(sum(exLength))
    ptLength.append(sum(ptLength))

    return restList, capList, restLength, exLength, ptLength

def summarize(inShp, outCsv):
    restLabels, capLabels, restValues, exValues, ptValues = readShp(inShp)
    colLabels = ['Category', 'Length', 'Percent']

    file = open(outCsv, 'wb')
    writer = csv.writer(file)

    writer.writerow(['BRAT Restoration'])
    writer.writerow(colLabels)
    for i in range(0, len(restLabels), 1):
        rowList = [restLabels[i], restValues[i], restValues[i]/restValues[-1]*100.0]
        writer.writerow(rowList)
    writer.writerow(['BRAT Existing'])
    writer.writerow(colLabels)
    for i in range(0, len(capLabels), 1):
        rowList = [capLabels[i], exValues[i], exValues[i]/exValues[-1]*100.0]
        writer.writerow(rowList)
    writer.writerow(['BRAT Potential'])
    writer.writerow(colLabels)
    for i in range(0, len(capLabels), 1):
        rowList = [capLabels[i], ptValues[i], ptValues[i]/ptValues[-1]*100.0]
        writer.writerow(rowList)

    file.close()

path = r'E:\etal\Projects\USA\Utah\BRAT\SageGrouse\BRAT_SG_BoxElder.shp'
csvPath = r'C:\Users\khafe\Desktop\brat.csv'
summarize(path, csvPath)