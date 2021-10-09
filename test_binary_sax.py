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

# I have created a function to extend SAX words to any arbitrary number
# by making the characters bit strins

import math
import itertools



def countBits(number):
    return int((math.log(number) / math.log(2)) + 1)

# # Driver Code
# num = 5

# print(countBits(num))


def bit_sequence(bits_needed, number):
    bit_sequence = []
    bin_num = str(bin(number - 1))[2:]
    for x in map(''.join, itertools.product('01', repeat=bits_needed)):
        print(f"{bin_num}, {x}")
        bit_sequence.append(x)
        if bin_num == x:
            break

    return bit_sequence


num = 5
print(countBits(num))
print(bit_sequence(countBits(num), num))
