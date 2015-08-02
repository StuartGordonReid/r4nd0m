__author__ = 'x433165'


from BinaryFrame import BinaryFrame
import scipy.special as spc
import math


class RandomnessTester:
    def __init__(self, bin):
        assert isinstance(bin, BinaryFrame)
        self.bin = bin

    def mono_bit_test(self):
        for c in self.bin.columns:
            str_data = self.bin.bin_data[c]
            count = 0
            for char in str_data:
                if char == '0':
                    count -= 1
                else:
                    count += 1
            sobs = count/math.sqrt(len(str_data))
            p_val = spc.erfc(math.fabs(sobs)/math.sqrt(2))
            if p_val < 0.01:
                print(c, "FAIL Monobit Test", '%.16f' % p_val, '%.16f' % sobs)
            else:
                print(c, "PASS Monobit Test", '%.16f' % p_val, '%.16f' % sobs)