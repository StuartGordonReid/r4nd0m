__author__ = 'x433165'

from BinaryFrame import BinaryFrame
import scipy.special as spc
import numpy
import math


class Colours:
    Pass = '\033[92m'
    Fail = '\033[91m'
    End = '\033[0m'
    Bold = '\033[1m'


class RandomnessTester:
    def __init__(self, bin):
        assert isinstance(bin, BinaryFrame)
        self.bin = bin

    def print_result(self, test_name, data_name, p_val, boundary=0.01):
        if p_val < boundary:
            print("\t", Colours.Bold + Colours.Fail + data_name + "\tFAIL! \t" +
                  Colours.End + Colours.Fail + test_name, ";",
                  "p value =", '%.6f' % p_val + Colours.End)
        else:
            print("\t", Colours.Bold + Colours.Pass + data_name + "\tPASS! \t" +
                  Colours.End + Colours.Pass + test_name, ";",
                  "p value =", '%.6f' % p_val + Colours.End)

    def monobit_test(self):
        for c in self.bin.columns:
            str_data = self.bin.bin_data[c]
            count = 0
            for char in str_data:
                if char == '0':
                    count -= 1
                else:
                    count += 1
            sobs = count / math.sqrt(len(str_data))
            p_val = spc.erfc(math.fabs(sobs) / math.sqrt(2))
            self.print_result("Monobit Test", c, p_val)

    def block_frequency_test(self, block_size):
        for c in self.bin.columns:
            str_data = self.bin.bin_data[c]
            num_blocks = int(len(str_data) / block_size)
            block_start, block_end = 0, block_size
            proportions = numpy.zeros(num_blocks)
            for i in range(num_blocks):
                block_data = str_data[block_start:block_end]
                ones_count = 0
                for char in block_data:
                    if char == '1':
                        ones_count += 1
                proportions[i] = ones_count / block_size
                block_start += block_size
                block_end += block_size
            chi = (proportions - 0.5)**2
            stat = 4 * block_size * numpy.sum(chi)
            p_val = spc.gammainc(num_blocks/2, stat/2)
            self.print_result("Block Frequency Test", c, p_val)
