import math
import bitstring


class BinaryFrame:
    def __init__(self, data, start, end, years_per_block):
        """
        Initialization method for a Binary Frame object
        :param data: a pandas DataFrame to convert
        """
        self.data = data
        self.bin_data = {}
        self.time_periods = math.floor((end - start) / years_per_block)
        self.columns = self.data.columns
        self.method = "discretize"

    def convert(self, method, convert=True):
        """
        A method for discretizing a pandas DataFrame into a Dictionary of Binary Strings
        1) If the return is +, then set the equivalent bit to 1
        2) If the return is -, then set the equivalent bit to 0
        Note that using this method compresses the data significantly
        :return:
        """
        # For each data set i.e. security return sequences
        for data_set in self.data.columns:
            # List of binary streams
            binary_streams = []
            # Days stepped through
            day_counter = 0
            # Total number of days i.e. returns
            days = len(self.data[data_set])
            # Days per binary stream
            days_in_stream = math.floor(days / self.time_periods)
            # print("\t", "Converting", data_set, "to BinaryFrame. Days in stream =", days_in_stream)
            # While less binary streams than time periods
            while len(binary_streams) < self.time_periods:
                # Start a new binary stream
                binary_stream = ""
                # Convert each day into binary
                for j in range(days_in_stream):
                    bit = ""
                    if method == "discretize":
                        bit = self.discretize(self.data[data_set][day_counter])
                    elif method == "convert basis point":
                        bit = self.convert_basis_point(self.data[data_set][day_counter], convert)
                    elif method == "convert floating point":
                        bit = self.convert_floating_point(self.data[data_set][day_counter])
                    else:
                        print("Unknown conversion method ... exiting application")
                        exit(0)
                    # Keep tack of days
                    day_counter += 1
                    # Add day to binary stream
                    binary_stream += bit
                # Append binary stream to binary streams list
                binary_streams.append(binary_stream)
            # Set the binary data for this data set to the binary streams list
            self.bin_data[data_set] = binary_streams

    def discretize(self, fp):
        """
        This method discretizes the floating point number according to whether it is + or -
        :param fp: the floating point number to convert
        :return: a binary string
        """
        if fp > 0.0:
            return '1'
        if fp < 0.0:
            return '0'
        if fp == 0.0:
            return '01'

    def convert_basis_point(self, fp, convert=True):
        """
        This method converts a floating point number to an integer (basis points) and then converts it to binary
        :param fp: floating point number
        :param convert: if true, then the number is not already an integer
        :return: a binary string
        """
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
        """
        This method converts a floating point number into a binary string using the IEEE 754 method
        :param fp: floating point number
        :param length: the length of the resulting bit string
        :return: a binary string
        """
        bin_r = bitstring.BitArray(float=fp, length=length)
        bits = str(bin_r._getbin())[1:]
        if fp > 0.0:
            return '1' + bits
        elif fp < 0.0:
            return '0' + self.flip_bits(bits)
        else:
            return '01'

    def flip_bits(self, bit):
        """
        This method flips the bits in a binary string
        :param bit: the binary string
        :return:
        """
        bit = bit.replace('1', '2')
        bit = bit.replace('0', '1')
        return bit.replace('2', '0')
