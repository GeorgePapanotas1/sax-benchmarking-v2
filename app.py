import sys
import numpy as np
import json
import pandas as pd
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize


def handler(event, context):
    rng = np.random.RandomState(10)
    X = rng.randn(1000, 12).ravel
    return "json.dumps(X.tolist())"


def generateTimeseries(sizeOfDatasets):
    timeseries = np.random.rand(sizeOfDatasets)
    f = lambda x: x * 10
    timeseries = f(timeseries)
    return timeseries


def createdatasets(numberOfDatasets, datasetSize):
    datasets = np.zeros(shape=(numberOfDatasets, datasetSize))
    for i in range(len(datasets)):
        datasets[i] = generateTimeseries(datasetSize)
    return datasets


def convert_to_sax(dat, word_size, alphabet_size):
    dat_znorm = znorm(dat)
    dat_paa_3 = paa(dat_znorm, word_size)
    sax_string = ts_to_string(dat_paa_3, cuts_for_asize(alphabet_size))
    return sax_string


def collect_results(datasets, word_size, alphabet_size):
    sax_words = []
    print(sax_words)
    for i in range(len(datasets)):
        print(f"Indexing dataset {i} of {len(datasets)}")
        sax_words.append(convert_to_sax(datasets[i], word_size, alphabet_size))
        print(f"Result: {sax_words[i]}")
    return sax_words

word_size, alphabet_size = 120, 25

print(collect_results(createdatasets(1, 500), word_size, alphabet_size))

# At this state we are able to create X datasets of Y length and convert them to SAX words of w, a
# The next problem is the compare strategy.
# Compare every string with each other?
# Perform sampled comparisons?
# Perform a fixed number of comparisons?
# I should ask prof Kotidis about this.
# Another question is what data to collect. Okay, we run the comparisons with w, a. What is the desired result?
