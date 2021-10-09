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


def countBits(number):
    return int((math.log(number) / math.log(2)) + 1)


def bit_sequence(bits_needed, number):
    bit_sequence = []
    bin_num = str(bin(number - 1))[2:]
    for x in map(''.join, itertools.product('01', repeat=bits_needed)):
        bit_sequence.append(x)
        if bin_num == x:
            break

    return bit_sequence


def ts_to_string(series, cuts):
    """A straightforward num-to-string conversion."""
    a_size = len(cuts)
    sax = list()

    #  Create the bit array.
    sudo_bits = bit_sequence(countBits(a_size), a_size)

    for i in range(0, len(series)):
        num = series[i]
        # if teh number below 0, start from the bottom, or else from the top
        if num >= 0:
            j = a_size - 1
            while (j > 0) and (cuts[j] >= num):
                j = j - 1
            sax.append(chr(97 + j) if a_size < 20 else sudo_bits[j])
        else:
            j = 1
            while j < a_size and cuts[j] <= num:
                j = j + 1
            sax.append(chr(97 + (j-1)) if a_size < 20 else sudo_bits[j-1])
    return "".join(sax) if a_size < 20 else np.array(sax)


def convert_to_sax(dat, word_size, alphabet_size):
    dat_znorm = znorm(dat)
    dat_paa_3 = paa(dat_znorm, word_size)
    sax_string = ts_to_string(dat_paa_3, cuts_for_asize(alphabet_size))
    return sax_string


def cuts_for_asize(num):
    cuts = [-np.inf]
    for i in range(1, num):
        cuts.append(norm.ppf(i * 1/num))
    return cuts


word_size, alphabet_size = 50, 21

df = pd.read_csv ('first_year_subset.csv')
dat1 = df['Temp'].to_numpy()
sax1 = convert_to_sax(dat1, word_size, alphabet_size)

print(len(dat1))
print(len(sax1))

