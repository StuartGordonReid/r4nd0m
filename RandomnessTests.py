__author__ = 'x433165'


from BinaryFrame import BinaryFrame
import scipy.special as spc
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
                print("\t", Colours.Bold + Colours.Fail + c + "\tFAIL! \t" +
                      Colours.End + Colours.Fail + "Monobit Test", ";",
                      "p value =", '%.6f' % p_val, ";",
                      "sobs value =", '%.6f' % sobs + Colours.End)
            else:
                print("\t", Colours.Bold + Colours.Pass + c + "\tPASS! \t" +
                      Colours.End + Colours.Pass + "Monobit Test", ";",
                      "p value =", '%.6f' % p_val, ";",
                      "sobs value =", '%.6f' % sobs + Colours.End)
