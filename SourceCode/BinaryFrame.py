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
        self.time = end - start
        self.years_per_block = years_per_block
        self.time_periods = math.floor(self.time / years_per_block)
        self.time_periods_fwd = math.floor(self.time - years_per_block + 1)
        # print(self.time_periods, self.time_periods_fwd)
        self.columns = self.data.columns
        self.method = "discretize"

    def convert(self, method, convert=True, independent_samples=True):
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
            day = 0
            days = len(self.data[data_set])
            days_in_stream = math.floor(days / self.time_periods)
            days_in_year = math.floor(days / self.time)
            # While less binary streams than time periods
            samples = self.time_periods
            if not independent_samples:
                samples = self.time_periods_fwd
            while len(binary_streams) < samples:
                # Start a new binary stream
                binary_stream = ""
                # Convert each day into binary
                for j in range(day, (day + days_in_stream)):
                    bit = ""
                    if method == "discretize":
                        bit = self.discretize(self.data[data_set][j])
                    elif method == "convert basis point":
                        bit = self.convert_basis_point(self.data[data_set][j], convert)
                    elif method == "convert floating point":
                        bit = self.convert_floating_point(self.data[data_set][j])
                    else:
                        print("Unknown conversion method ... exiting application")
                        exit(0)
                    # Add day to binary stream
                    binary_stream += bit
                    # Keep tack of days
                    if independent_samples:
                        day += 1
                if not independent_samples:
                    day += days_in_year
                # Append binary stream to binary streams list
                binary_streams.append(binary_stream)
            # Set the binary data for this data set to the binary streams list
            self.bin_data[data_set] = binary_streams

    def discretize(self, floating_point):
        """
        This method discretizes the floating point number according to whether it is + or -
        :param floating_point: the floating point number to convert
        :return: a binary string
        """
        if floating_point > 0.0:
            return '1'
        if floating_point < 0.0:
            return '0'
        if floating_point == 0.0:
            return '01'

    def convert_basis_point(self, floating_point, convert=True):
        """
        This method converts a floating point number to an integer (basis points) and then converts it to binary
        :param floating_point: floating point number
        :param convert: if true, then the number is not already an integer
        :return: a binary string
        """
        if convert:
            floating_point = int(floating_point * 100)
        bstring = bin(floating_point)
        if floating_point > 0.0:
            return '1' + str(bstring[2:])
        elif floating_point < 0.0:
            return '0' + self.flip_bits(str(bstring[3:]))
        else:
            return '01'

    def convert_floating_point(self, floating_point, length=64):
        """
        This method converts a floating point number into a binary string using the IEEE 754 method
        :param floating_point: floating point number
        :param length: the length of the resulting bit string
        :return: a binary string
        """
        bin_r = bitstring.BitArray(float=floating_point, length=length)
        bits = str(bin_r._getbin())[1:]
        if floating_point > 0.0:
            return '1' + bits
        elif floating_point < 0.0:
            return '0' + self.flip_bits(bits)
        else:
            return '01'

    def flip_bits(self, bin_data):
        """
        This method flips the bits in a binary string
        :param bin_data: the binary string
        :return:
        """
        bin_data = bin_data.replace('1', '2')
        bin_data = bin_data.replace('0', '1')
        return bin_data.replace('2', '0')
