from BinaryFrame import BinaryFrame
import scipy.special as spc
import numpy
import math


class Colours:
    """
    Just used to make the standard-out a little bit less ugly
    """
    Pass, Fail, End, Bold, Info = '\033[92m', '\033[91m', '\033[0m', '\033[1m', '\033[94m'


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
            return False
        else:
            print("\t", Colours.Bold + Colours.Pass + data_name + "\tPASS! \t" +
                  Colours.End + Colours.Pass + test_name, ";",
                  "p value =", '%.6f' % p_val + Colours.End)
            return True

    def run_test_suite(self, block_size):
        for c in self.bin.columns:
            print("\t", Colours.Bold + "Running tests for", c + Colours.End)
            str_data = self.bin.bin_data[c]
            monobit_result = self.monobit_test(str_data, c)
            if monobit_result:
                block_frequency_result = self.block_frequency_test(str_data, c, block_size)
                if block_frequency_result:
                    runs_result = self.runs_test(str_data, c)
                    if runs_result:
                        self.pass_tests()
                else:
                    self.fail_tests()
            else:
                self.fail_tests()

    def fail_tests(self):
        print("\t", Colours.Bold + "Failing all subsequent tests" + Colours.End)

    def pass_tests(self):
        print("\t", Colours.Bold + "Passed all randomness tests" + Colours.End)

    def monobit_test(self, str_data, column):
        """
        **From the NIST documentation**
        The focus of this test is the proportion of zeros and ones for the entire sequence. The purpose of this test is
        to determine whether the number of ones and zeros in a sequence are approximately the same as would be expected
        for a truly random sequence. This test assesses the closeness of the fraction of ones to 1/2, that is the number
        of ones and zeros ina  sequence should be about the same. All subsequent tests depend on this test.
        """
        count = 0
        # If the char is 0 minus 1, else add 1
        for char in str_data:
            if char == '0':
                count -= 1
            else:
                count += 1
        # Calculate the p value
        sobs = count / math.sqrt(len(str_data))
        p_val = spc.erfc(math.fabs(sobs) / math.sqrt(2))
        return self.print_result("Monobit Test", column, p_val)

    def block_frequency_test(self, str_data, column, block_size):
        """
        **From the NIST documentation**
        The focus of this tests is the proportion of ones within M-bit blocks. The purpose of this tests is to determine
        whether the frequency of ones in an M-bit block is approximately M/2, as would be expected under an assumption
        of randomness. For block size M=1, this test degenerates to the monobit frequency test.
        :param block_size: the size of the blocks that the binary sequence is partitioned into
        """
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
        chi = (proportions - 0.5) ** 2
        stat = 4 * block_size * numpy.sum(chi)
        p_val = spc.gammainc(num_blocks / 2, stat / 2)
        return self.print_result("Block Frequency Test", column, p_val)

    def runs_test(self, str_data, column):
        ones_count, n = 0, len(str_data)
        for char in str_data:
            if char == '1':
                ones_count += 1
        proportion, vobs = float(ones_count / n), 0
        for i in range(n - 2):
            if str_data[i] != str_data[i + 1]:
                vobs += 1
        num = (vobs - (2 * n * proportion * (1 - proportion)))
        den = (2 * math.sqrt(2 * n) * proportion * (1 - proportion))
        p_val = spc.erfc(num/den)
        return self.print_result("Runs Test", column, p_val)
