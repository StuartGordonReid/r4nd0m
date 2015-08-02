import bitstring
import pandas
import numpy


class BinaryFrame:
    def __init__(self, data):
        """
        Initialization method for a Binary Frame object
        :param data: a pandas DataFrame to convert
        """
        assert isinstance(data, pandas.DataFrame)
        self.data = data
        self.bin_data = {}
        self.columns = self.data.columns

    def convert_unbiased(self):
        """
        A method for converting a floating point binary pandas DataFrame into a Dictionary of binary strings
        1) Convert the floating points as per the IEEE 754 standard
        2) Check if the first bit is 1 or 0 (+ or -)
        3) If negative flip the bits in the string
        4) Special case - if the floating point number is 0, then return an unbiased string
        :return:
        """
        for c in self.data.columns:
            cbin_data = ""
            for i in range(len(self.data[c])):
                if self.data[c][i] != 0.0:
                    bin_r = bitstring.BitArray(float=self.data[c][i], length=64)
                    bit_string = str(bin_r._getbin())
                    if bit_string[0] == '1':
                        bit_string = bit_string[1::]
                        bit_string = bit_string.replace('1', '2').replace('0', '1').replace('2', '0')
                        bit_string = '1' + bit_string
                    cbin_data += bit_string
                else:
                    cbin_data += "0101010101010101010101010101010101010101010101010101010101010101"
            self.bin_data[c] = cbin_data

    def discretize(self):
        """
        A method for discretizing a pandas DataFrame into a Dictionary of Binary Strings
        1) If the return is +, then set the equivalent bit to 1
        2) If the return is -, then set the equivalent bit to 0
        Note that using this method compresses the data significantly
        :return:
        """
        for c in self.data.columns:
            cbin_data = ""
            for i in range(len(self.data[c])):
                if self.data[c][i] >= 0.0:
                    cbin_data += '1'
                else:
                    cbin_data += '0'
            self.bin_data[c] = cbin_data


def test_unbiased_conversion():
    f, sum_one, sum_zero = -1.0, 0, 0
    bit_count = numpy.zeros(63)
    for i in range(21):
        if f != 0.0:
            bin_r = bitstring.BitArray(float=f, length=64)
            bstring = str(bin_r._getbin())

            if bstring[0] == '1':
                bstring = bstring[1::]
                bstring = bstring.replace('1', '2').replace('0', '1').replace('2', '0')
                bstring = '1' + bstring

            z = bstring.count("0")
            o = bstring.count("1")
            sum_one += o
            sum_zero += z

            for j in range(63):
                bit_count[j] += int(bstring[j])

            print(f, "\t", bstring, z, o)
        f = round(f + 0.1, 1)

    print(sum_one, sum_zero, sum_zero-sum_one)
    print(bit_count)


if __name__ == '__main__':
    test_unbiased_conversion()
