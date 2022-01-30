import random
import shutil
import zipfile
import glob as g
import os
import pandas as pd
import numpy as np


class DatasetHelper:
    path = "./FinancialData/history"
    exports = "./FinancialData/exports"
    fitness = "./FinancialData/fitness"
    min_similarity = 0.80
    max_tries = 20

    def __init__(self):
        self.changeDataset = False

    @staticmethod
    def pickRandomFiles(index, limit):
        first = random.randint(index, limit - 1)
        second = random.randint(index, limit - 1)
        while first == second:
            second = random.randint(index, limit - 1)
        return [first, second]

    @staticmethod
    def pickRandomIndex(index, limit):
        return random.randint(index, limit - 1)

    @staticmethod
    def purgeExports(dirToRemove):
        try:
            shutil.rmtree(dirToRemove)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    @staticmethod
    def extractSingleZip(pathToFile, pathToExport, file):
        with zipfile.ZipFile(pathToFile + "/" + file, 'r') as zip_ref:
            zip_ref.extractall(pathToExport)

    def extractData(self, pathToFiles, pathToExport, files):
        for f in files:
            self.extractSingleZip(pathToFiles, pathToExport, f)

    @staticmethod
    def getExported(exportPath):
        return g.glob(exportPath + "/*")

    def fetchTimeseriesFiles(self, change_dataset):
        path = self.path
        exports = self.exports
        if change_dataset:
            self.purgeExports(exports)
            datasetFiles = os.listdir(path)
            [firstFileIndex, secondFileIndex] = self.pickRandomFiles(0, len(datasetFiles))
            self.extractData(path, exports, [datasetFiles[firstFileIndex], datasetFiles[secondFileIndex]])
        return self.getExported(exports)

    @staticmethod
    def calculateSimilarity(t1, t2):
        return min(t1, t2) / max(t1, t2)

    @staticmethod
    def calculateTimeseriesFitness(self, control, datasetFiles, currentPair):
        export = self.exports+'/pair'+str(currentPair)
        self.extractData(self.path, export, [datasetFiles[control]])
        control_timeseries = pd.read_csv(self.getExported(export)[0], sep=',',
                                         names=["id", "time", "price", "volume"])
        ct = control_timeseries['price'].to_numpy()
        similarity = 0
        tries = 0
        while similarity < self.min_similarity and tries < self.max_tries:
            test = control
            while test == control:
                test = self.pickRandomIndex(0, len(datasetFiles))
            self.extractData(self.path, self.fitness, [datasetFiles[test]])

            testing_timeseries = pd.read_csv(self.getExported(self.fitness)[0], sep=',',
                                             names=["id", "time", "price", "volume"])

            tt = testing_timeseries['price'].to_numpy()

            current_sim = self.calculateSimilarity(len(ct), len(tt))
            if current_sim < self.min_similarity:
                self.purgeExports(self.fitness)
            similarity = current_sim
            tries += 1

        if similarity < self.min_similarity:
            return False
        else:
            pair = os.listdir(self.fitness)[0]
            shutil.move(self.fitness + '/' + pair, self.exports + '/pair' + str(currentPair) + '/' + pair)
            self.purgeExports(self.fitness)
            return True

    def reset(self):
        self.purgeExports(self.exports)
        self.purgeExports(self.fitness)

    def findTimeseriesPairs(self, changeDataset, numberOfPairs):
        if changeDataset:
            self.purgeExports(self.exports)
            datasetFiles = os.listdir(self.path)
            for i in range(numberOfPairs):
                pairFound = False
                while not pairFound:
                    self.purgeExports(self.exports + '/pair' + str(i))
                    control = self.pickRandomIndex(0, len(datasetFiles))
                    pairFound = self.calculateTimeseriesFitness(self, control, datasetFiles, i)

    def getTimeseriesPairs(self):
        dirs = os.listdir(self.exports)
        t = []
        for i in dirs:
            files = os.listdir(self.exports+'/'+i)
            t.append([self.exports+'/'+i+"/"+files[0], self.exports+'/'+i+"/"+files[1]])
        return t
