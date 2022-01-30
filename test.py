from classes.DatasetHelper import DatasetHelper
from classes.SaxHelper import SaxHelper
from sys import getsizeof


# datasetHelper.findTimeseriesPairs(True, 5)


def handler(word_length, alphabet_size, files):
    word_size, alphabet_size = word_length, alphabet_size
    saxHelper = SaxHelper()
    sax1, sax2, dat1, dat2, od = saxHelper.newConvertRawToSax(word_size, alphabet_size, files)

    print("Tightness of Lower bound: ", saxHelper.calculateSaxDistance(sax1, sax2, alphabet_size) / od)
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


def performTest(word_length, alphabet_size, changeDataset=False, numberOfPairs=1):
    datasetHelper = DatasetHelper()

    if changeDataset:
        datasetHelper.findTimeseriesPairs(True, numberOfPairs)

    for i in datasetHelper.getTimeseriesPairs():
        handler(word_length, alphabet_size, i)


performTest(500, 6, True, 10)
