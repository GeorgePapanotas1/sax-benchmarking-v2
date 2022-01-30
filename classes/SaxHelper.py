import math
import itertools
from saxpy.znorm import znorm
from saxpy.paa import paa
import pandas as pd
from scipy.stats import norm
import numpy as np
import string


class SaxHelper:

    def countBits(self, number):
        return int((math.log(number) / math.log(2)) + 1)

    def bit_sequence(self, bits_needed, number, retType):
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

    def ts_to_string(self, series, cuts):
        """A straightforward num-to-string conversion."""
        a_size = len(cuts)
        sax = list()

        #  Create the bit array.
        sudo_bits = self.bit_sequence(self.countBits(a_size), a_size, 'str')

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

    def convert_to_sax(self, dat, word_size, alphabet_size):
        dat_znorm = znorm(dat)
        dat_paa_3 = paa(dat_znorm, word_size)
        sax_string = self.ts_to_string(dat_paa_3, self.cuts_for_asize(alphabet_size))
        return sax_string

    @staticmethod
    def cuts_for_asize(num):
        cuts = [-np.inf]
        for i in range(1, num):
            cuts.append(norm.ppf(i * 1 / num))
        return cuts

    def convertRawToSax(self, word_size, alphabet_size, files):
        return_list = []
        dat_list = []
        for f in files:
            df = pd.read_csv(f, sep=',', names=["id", "time", "price", "volume"])
            dat = df['price'].to_numpy()
            dat_list.append(dat)
            sax = self.convert_to_sax(dat, word_size, alphabet_size)
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

    def newConvertRawToSax(self, word_size, alphabet_size, files):
        return_list = []
        dat_list = []
        for f in files:
            df = pd.read_csv(f, sep=',', names=["id", "time", "price", "volume"])
            dat = df['price'].to_numpy()
            dat_list.append(dat)

        if len(dat_list[0]) < len(dat_list[1]):
            dat_list[1] = dat_list[1][:len(dat_list[0])]
        else:
            dat_list[0] = dat_list[0][:len(dat_list[1])]

        for dat in dat_list:
            sax = self.convert_to_sax(dat, word_size, alphabet_size)
            return_list.append(sax)

        return_list.append(dat_list[0])
        return_list.append(dat_list[1])
        od = np.linalg.norm(dat_list[0] - dat_list[1])
        return_list.append(od)
        return return_list

    def calculateMinDistTable(self, alpabet_s):
        mindist = np.empty([alpabet_s, alpabet_s])
        breakpoints = self.cuts_for_asize(alpabet_s)
        for x in range(alpabet_s):
            for y in range(alpabet_s):
                if abs(x - y) <= 1:
                    mindist[x, y] = 0
                else:
                    mindist[x, y] = breakpoints[max(x + 1, y + 1) - 1] - breakpoints[min(x + 1, y + 1)]
        return mindist

    def calculateSaxDistance(self, sax1, sax2, alph_size):
        if alph_size < 20:
            alph = string.ascii_lowercase[0:alph_size]
        else:
            alph = self.bit_sequence(self.countBits(alph_size), alph_size, 'bin')
        sax_distance = 0
        mindist = self.calculateMinDistTable(alph_size)
        print(alph)
        for i in range(len(sax1)):
            sax1_index = alph.index(sax1[i])
            sax2_index = alph.index(sax2[i])
            sax_distance = sax_distance + mindist[sax1_index, sax2_index]
        print("SAX Min Dist:", sax_distance)
        return sax_distance
