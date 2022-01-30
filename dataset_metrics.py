import glob as g
import shutil
import os
import random
import zipfile


def purgeExports(dirToRemove):
    try:
        shutil.rmtree(dirToRemove)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def getExported(exportPath):
    return g.glob(exportPath + "*")


def pickRandomFiles(index, limit):
    first = random.randint(index, limit - 1)
    second = random.randint(index, limit - 1)
    while first == second:
        second = random.randint(index, limit - 1)
    return [first, second]


def extractSingleZip(pathToFile, pathToExport, file):
    with zipfile.ZipFile(pathToFile + "/" + file, 'r') as zip_ref:
        zip_ref.extractall(pathToExport)


def extractData(pathToFiles, pathToExport, files):
    for f in files:
        extractSingleZip(pathToFiles, pathToExport, f)


def fetchTimeseriesFiles(change_dataset):
    path = "./FinancialData/history"
    exports = "./FinancialData/exports/"
    if change_dataset:
        purgeExports(exports)
        datasetFiles = os.listdir(path)
        [firstFileIndex, secondFileIndex] = pickRandomFiles(0, len(datasetFiles))
        extractData(path, exports, [datasetFiles[firstFileIndex], datasetFiles[secondFileIndex]])
    return getExported(exports)
