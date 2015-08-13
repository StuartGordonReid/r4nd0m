import bitstring


# TODO: Add more comments to this file


class BinaryFrame:
    def __init__(self, data, stream_size):
        """
        Initialization method for a Binary Frame object
        :param data: a pandas DataFrame to convert
        """
        self.data = data
        self.bin_data = {}
        self.stream_size = stream_size
        self.columns = self.data.columns
        self.method = "discretize"

    def convert(self, method="discretize", convert=True):
        """
        A method for discretizing a pandas DataFrame into a Dictionary of Binary Strings
        1) If the return is +, then set the equivalent bit to 1
        2) If the return is -, then set the equivalent bit to 0
        Note that using this method compresses the data significantly
        :return:
        """
        self.method = method
        for c in self.data.columns:
            cbin_data, index = [], 0
            while (len(self.data[c]) - index) > self.stream_size:
                bstring = ""
                while len(bstring) < self.stream_size:
                    bit = ""
                    if method == "discretize":
                        bit = self.discretize(self.data[c][index])
                    elif method == "convert basis point":
                        bit = self.convert_basis_point(self.data[c][index], convert)
                    elif method == "convert floating point":
                        bit = self.convert_floating_point(self.data[c][index])
                    else:
                        print("Unknown conversion method ... exiting application")
                        exit(0)
                    index += 1
                    bstring += bit
                cbin_data.append(bstring)
            self.bin_data[c] = cbin_data
            # print(len(cbin_data) * self.stream_size)

    def discretize(self, fp):
        if fp > 0.0:
            return '1'
        if fp < 0.0:
            return '0'
        if fp == 0.0:
            return '01'

    def convert_basis_point(self, fp, convert=True):
        if convert:
            fp = int(fp * 100)
        bstring = bin(fp)
        if fp > 0.0:
            return '1' + str(bstring[2:])
        elif fp < 0.0:
            return '0' + self.flip_bits(str(bstring[3:]))
        else:
            return '01'

    def convert_floating_point(self, fp, length=64):
        bin_r = bitstring.BitArray(float=fp, length=length)
        bits = str(bin_r._getbin())[1:]
        if fp > 0.0:
            return '1' + bits
        elif fp < 0.0:
            return '0' + self.flip_bits(bits)
        else:
            return '01'

    def flip_bits(self, bit):
        bit = bit.replace('1', '2')
        bit = bit.replace('0', '1')
        return bit.replace('2', '0')


if __name__ == '__main__':
    print("Nothing")
