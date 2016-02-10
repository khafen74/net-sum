from gdal import ogr
import os
import csv

def readConf(inShp):
    confList = ['0-0.10', '0.10-0.25', '0.25-0.50', '0.50-0.75', '0.75-1.0', 'Total']
    confVals = [0.0]*5
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
        pConf = feat.GetField('oPC_Prob')
        featLen = feat.GetField('iGeo_Lengt')

        if pConf <= 0.1 and pConf > 0.0:
            confVals[0] += featLen
        elif pConf <= 0.25 and pConf > 0.1:
            confVals[1] += featLen
        elif pConf <= 0.5 and pConf > 0.25:
            confVals[2] += featLen
        elif pConf <= 0.75 and pConf > 0.5:
            confVals[3] += featLen
        elif pConf <= 1.0 and pConf > 0.75:
            confVals[4] += featLen
        else:
            print 'pconf error, out of acceptable range'

    confVals.append(sum(confVals))

    return confList, confVals

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
    confLabels, confValues = readConf(inShp)
    colLabels = ['Category', 'Length', 'Percent']

    file = open(outCsv, 'wb')
    writer = csv.writer(file)

    writer.writerow(['BRAT Restoration'])
    writer.writerow(colLabels)
    for i in range(0, len(restLabels), 1):
        rowList = [restLabels[i], restValues[i], restValues[i]/restValues[-1]]
        writer.writerow(rowList)
    writer.writerow(['BRAT Existing'])
    writer.writerow(colLabels)
    for i in range(0, len(capLabels), 1):
        rowList = [capLabels[i], exValues[i], exValues[i]/exValues[-1]]
        writer.writerow(rowList)
    writer.writerow(['BRAT Potential'])
    writer.writerow(colLabels)
    for i in range(0, len(capLabels), 1):
        rowList = [capLabels[i], ptValues[i], ptValues[i]/ptValues[-1]]
        writer.writerow(rowList)
    writer.writerow(['BRAT Conflict'])
    writer.writerow(colLabels)
    for i in range(0, len(confLabels), 1):
        rowList = [confLabels[i], confValues[i], confValues[i]/confValues[-1]]
        writer.writerow(rowList)

    file.close()

path = r'E:\etal\Projects\USA\Utah\BRAT\SageGrouse\BRAT_SG_BoxElder.shp'
csvPath = r'C:\Users\khafe\Desktop\bratconf_be.csv'
summarize(path, csvPath)