# I have created a function to extend SAX words to any arbitrary number
# by making the characters bit strins

import math
import sys
import itertools
from saxpy.znorm import znorm
from saxpy.paa import paa
import pandas as pd
from scipy.stats import norm
import numpy as np
import os
import random
import zipfile
import shutil
import glob as g
import string
from sys import getsizeof


def countBits(number):
    return int((math.log(number) / math.log(2)) + 1)


def bit_sequence(bits_needed, number, retType):
    bit_sequence = []
    bin_num = str(bin(number - 1))[2:]
    for x in map(''.join, itertools.product('01', repeat=bits_needed)):
        if retType == 'bin':
            bit_sequence.append(bin(int(x, 2)))
        else:
            bit_sequence.append(x)
        if bin_num == x:
            break

    return bit_sequence


def ts_to_string(series, cuts):
    """A straightforward num-to-string conversion."""
    a_size = len(cuts)
    sax = list()

    #  Create the bit array.
    sudo_bits = bit_sequence(countBits(a_size), a_size, 'str')

    for i in range(0, len(series)):
        num = series[i]
        # if teh number below 0, start from the bottom, or else from the top
        if num >= 0:
            j = a_size - 1
            while (j > 0) and (cuts[j] >= num):
                j = j - 1
            sax.append(chr(97 + j) if a_size < 20 else bin(int(sudo_bits[j], 2)))
        else:
            j = 1
            while j < a_size and cuts[j] <= num:
                j = j + 1
            sax.append(chr(97 + (j - 1)) if a_size < 20 else bin(int(sudo_bits[j - 1], 2)))
    return "".join(sax) if a_size < 20 else np.array(sax)


def convert_to_sax(dat, word_size, alphabet_size):
    dat_znorm = znorm(dat)
    dat_paa_3 = paa(dat_znorm, word_size)
    sax_string = ts_to_string(dat_paa_3, cuts_for_asize(alphabet_size))
    return sax_string


def cuts_for_asize(num):
    cuts = [-np.inf]
    for i in range(1, num):
        cuts.append(norm.ppf(i * 1 / num))
    return cuts


def pickRandomFiles(index, limit):
    first = random.randint(index, limit - 1)
    second = random.randint(index, limit - 1)
    while first == second:
        second = random.randint(index, limit - 1)
    return [first, second]


def purgeExports(dirToRemove):
    try:
        shutil.rmtree(dirToRemove)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def extractSingleZip(pathToFile, pathToExport, file):
    with zipfile.ZipFile(pathToFile + "/" + file, 'r') as zip_ref:
        zip_ref.extractall(pathToExport)


def extractData(pathToFiles, pathToExport, files):
    for f in files:
        extractSingleZip(pathToFiles, pathToExport, f)


def getExported(exportPath):
    return g.glob(exportPath + "*")


def fetchTimeseriesFiles(change_dataset):
    path = "./FinancialData/history"
    exports = "./FinancialData/exports/"
    if change_dataset:
        purgeExports(exports)
        datasetFiles = os.listdir(path)
        [firstFileIndex, secondFileIndex] = pickRandomFiles(0, len(datasetFiles))
        extractData(path, exports, [datasetFiles[firstFileIndex], datasetFiles[secondFileIndex]])
    return getExported(exports)


def convertRawToSax(word_size, alphabet_size, files):
    return_list = []
    dat_list = []
    for f in files:
        df = pd.read_csv(f, sep=',', names=["id", "time", "price", "volume"])
        dat = df['price'].to_numpy()
        dat_list.append(dat)
        sax = convert_to_sax(dat, word_size, alphabet_size)
        return_list.append(sax)
    # Calculate difference
    if len(dat_list[0]) - len(dat_list[1]) > 0:
        diff = len(dat_list[0]) - len(dat_list[1])
        a = np.zeros((1, diff))
        dat_list[1] = np.append(dat_list[1], a)
    else:
        diff = len(dat_list[1]) - len(dat_list[0])
        a = np.zeros((1, diff))
        dat_list[0] = np.append(dat_list[0], a)
    return_list.append(dat_list[0])
    return_list.append(dat_list[1])
    od = np.linalg.norm(dat_list[0] - dat_list[1])
    return_list.append(od)
    return return_list


def calculateMinDistTable(alpabet_s):
    mindist = np.empty([alpabet_s, alpabet_s])
    breakpoints = cuts_for_asize(alpabet_s)
    for x in range(alpabet_s):
        for y in range(alpabet_s):
            if abs(x - y) <= 1:
                mindist[x, y] = 0
            else:
                mindist[x, y] = breakpoints[max(x + 1, y + 1) - 1] - breakpoints[min(x + 1, y + 1)]
    return mindist


def calculateSaxDistance(sax1, sax2, alph_size):
    if alph_size < 20:
        alph = string.ascii_lowercase[0:alph_size]
    else:
        alph = bit_sequence(countBits(alph_size), alph_size, 'bin')
    sax_distance = 0
    mindist = calculateMinDistTable(alph_size)
    print(alph)
    for i in range(len(sax1)):
        sax1_index = alph.index(sax1[i])
        sax2_index = alph.index(sax2[i])
        sax_distance = sax_distance + mindist[sax1_index, sax2_index]
    print("SAX Min Dist:", sax_distance)
    return sax_distance


# TODO 1. Wrap all values (saxes, dats, od, TLB, MinDist) to json and send to front end for reporting
# TODO 2. Reorganize the codebase.
# TODO 3. The execution time is unbearable. Try to multithread.
# TODO 4. Allow the user to modify the w, a coefficients via a front end and show results in the console.
# TODO 5. Create automated tests. For a pair of Timeseries run the code X times changing the w and a. Use a threshold

def handler(word_length, alphabet_size, change_dataset=False):
    word_size, alphabet_size = word_length, alphabet_size
    sax1, sax2, dat1, dat2, od = convertRawToSax(word_size, alphabet_size, fetchTimeseriesFiles(change_dataset))
    print("Tightness of Lower bound: ", calculateSaxDistance(sax1, sax2, alphabet_size) / od)
    print("Original Distance", od)
    if alphabet_size < 21:
        sax1_size = getsizeof(sax1)
        sax2_size = getsizeof(sax2)
    else:
        sax1_size = sax1.nbytes
        sax2_size = sax2.nbytes

    print("SAX 1 word size:", sax1_size, "--- Original timeseries size:", dat1.nbytes, "Compression ratio:", 100 - (
            sax1_size / dat1.nbytes) * 100)
    print("SAX 2 word size:", sax2_size, "--- Original timeseries size:", dat2.nbytes, "Compression ratio:", 100 - (
            sax2_size / dat2.nbytes) * 100)


handler(2000, 500, False)
