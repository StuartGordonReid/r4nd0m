__author__ = 'x433165'


import bitstring
import pandas
import numpy


class BinaryFrame:
    def __init__(self, data):
        assert isinstance(data, pandas.DataFrame)
        self.data = data
        self.bin_data = {}
        self.columns = self.data.columns

    def convert_int(self):
        for c in self.data.columns:
            cbin_data = ""
            for i in range(len(self.data[c])):
                int_r = abs(int((self.data[c][i]+0.0000001)*1000))
                bin_r = str(bin(int_r))[2:]
                # print(bin_r)
                cbin_data += bin_r
            self.bin_data[c] = cbin_data

    def convert_754(self):
        for c in self.data.columns:
            cbin_data = ""
            for i in range(len(self.data[c])):
                bin_r = bitstring.BitArray(float=self.data[c][i], length=32)
                cbin_data += str(bin_r._getbin())
            self.bin_data[c] = cbin_data

    def discretize(self):
        for c in self.data.columns:
            cbin_data = ""
            for i in range(len(self.data[c])):
                if self.data[c][i] >= 0.0:
                    cbin_data += '1'
                else:
                    cbin_data += '0'
            self.bin_data[c] = cbin_data


if __name__ == '__main__':
    f, sum_one, sum_zero = -1.0, 0, 0
    bit_count = numpy.zeros(31)
    for i in range(21):
        if f != 0.0:
            bin_r = bitstring.BitArray(float=f, length=32)
            bstring = str(bin_r._getbin())

            if bstring[0] == '1':
                bstring = bstring[1::]
                bstring = bstring.replace('1', '2').replace('0', '1').replace('2', '0')
                bstring = '1' + bstring

            z = bstring.count("0")
            o = bstring.count("1")
            sum_one += o
            sum_zero += z

            for j in range(31):
                bit_count[j] += int(bstring[j])

            print(f, "\t", bstring, z, o)
        f = round(f + 0.1, 1)

    print(sum_one, sum_zero, sum_zero-sum_one)
    print(bit_count)
