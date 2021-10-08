# def ts_to_string(series, cuts):
#     """A straightforward num-to-string conversion."""
#     a_size = len(cuts)
#     sax = list()
#     for i in range(0, len(series)):
#         num = series[i]
#         # if teh number below 0, start from the bottom, or else from the top
#         if(num >= 0):
#             j = a_size - 1
#             while ((j > 0) and (cuts[j] >= num)):
#                 j = j - 1
#             sax.append(idx2letter(j))
#         else:
#             j = 1
#             while (j < a_size and cuts[j] <= num):
#                 j = j + 1
#             sax.append(idx2letter(j-1))
#     return ''.join(sax)

# def calculateCardinality(wordLength):

import math


def countBits(number):
    return int((math.log(number) / math.log(2)) + 1)


# Driver Code
num = 5
print(countBits(num))
