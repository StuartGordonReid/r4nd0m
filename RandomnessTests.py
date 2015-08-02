from BinaryFrame import BinaryFrame
import scipy.special as spc
import numpy
import math


class Colours:
    """
    Just used to make the standard-out a little bit less ugly
    """
    Pass, Fail, End, Bold = '\033[92m', '\033[91m', '\033[0m', '\033[1m'


class RandomnessTester:
    def __init__(self, bin):
        """
        Initializes a randomness tester object for testing binary sequences for randomness
        :param bin: this is a "BinaryFrame" object which is a conversion of a pandas DataFrame into a binary dictionary
        """
        assert isinstance(bin, BinaryFrame)
        self.bin = bin

    def print_result(self, test_name, data_name, p_val, boundary=0.01):
        """
        This method prints the result of the randomness tests contained in this object
        :param test_name: the name of the test for randomness
        :param data_name: the name of the data-set (binary string) being tested
        :param p_val: the computer p-value from the test for randomness
        :param boundary: the decision boundary for pass / fail
        """
        if p_val < boundary:
            print("\t", Colours.Bold + Colours.Fail + data_name + "\tFAIL! \t" +
                  Colours.End + Colours.Fail + test_name, ";",
                  "p value =", '%.6f' % p_val + Colours.End)
        else:
            print("\t", Colours.Bold + Colours.Pass + data_name + "\tPASS! \t" +
                  Colours.End + Colours.Pass + test_name, ";",
                  "p value =", '%.6f' % p_val + Colours.End)

    def monobit_test(self):
        """
        **From the NIST documentation**
        The focus of this test is the proportion of zeros and ones for the entire sequence. The purpose of this test is
        to determine whether the number of ones and zeros in a sequence are approximately the same as would be expected
        for a truly random sequence. This test assesses the closeness of the fraction of ones to 1/2, that is the number
        of ones and zeros ina  sequence should be about the same. All subsequent tests depend on this test.
        """
        # For each data-set in the BinaryFrame
        for c in self.bin.columns:
            # Get the binary sequence and initialize the count
            str_data, count = self.bin.bin_data[c], 0
            # If the char is 0 minus 1, else add 1
            for char in str_data:
                if char == '0':
                    count -= 1
                else:
                    count += 1
            # Calculate the p value
            sobs = count / math.sqrt(len(str_data))
            p_val = spc.erfc(math.fabs(sobs) / math.sqrt(2))
            self.print_result("Monobit Test", c, p_val)

    def block_frequency_test(self, block_size):
        """
        **From the NIST documentation**
        The focus of this tests is the proportion of ones within M-bit blocks. The purpose of this tests is to determine
        whether the frequency of ones in an M-bit block is approximately M/2, as would be expected under an assumption
        of randomness. For block size M=1, this test degenerates to the monobit frequency test.
        :param block_size: the size of the blocks that the binary sequence is partitioned into
        """
        # For each data-set in the BinaryFrame
        for c in self.bin.columns:
            # Get the binary sequence and initialize the count
            str_data = self.bin.bin_data[c]
            # Work out the number of blocks, discard the remainder
            num_blocks = int(len(str_data) / block_size)
            block_start, block_end = 0, block_size
            # Keep track of the proportion of ones per block
            proportions = numpy.zeros(num_blocks)
            for i in range(num_blocks):
                # Slice the binary string into a block
                block_data = str_data[block_start:block_end]
                # Keep track of the number of ones
                ones_count = 0
                for char in block_data:
                    if char == '1':
                        ones_count += 1
                proportions[i] = ones_count / block_size
                # Update the slice locations
                block_start += block_size
                block_end += block_size
            # Calculate the p-value
            chi = (proportions - 0.5)**2
            stat = 4 * block_size * numpy.sum(chi)
            p_val = spc.gammainc(num_blocks/2, stat/2)
            self.print_result("Block Frequency Test", c, p_val)
