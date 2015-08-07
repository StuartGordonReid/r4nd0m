from BinaryFrame import BinaryFrame
import scipy.special as spc
import numpy.linalg as lng
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
        self.bin = bin
        self.epsilon = 0.0001
        self.test_data = "11001001000011111101101010100010001000010110100011" \
                         "00001000110100110001001100011001100010100010111000"
        self.test_data_8 = "11001100000101010110110001001100111000000000001001" \
                           "00110101010001000100111101011010000000110101111100" \
                           "1100111001101101100010110010"

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

    def run_test_suite_knockout(self, block_size: int):
        """
        This method runs all of the tests included in the NIST test suite for randomness
        :param block_size: the size of the blocks to look at
        """
        for c in self.bin.columns:
            print("\t", Colours.Bold + "Running tests for", c + Colours.End)
            str_data = self.bin.bin_data[c]
            monobit_result, p_val = self.monobit_test(str_data, c)
            if monobit_result:
                block_frequency_result, p_val = self.block_frequency_test(str_data, c, block_size)
                if block_frequency_result:
                    runs_result, p_val = self.runs_test(str_data, c)
                    if runs_result:
                        longest_run_result, p_val = self.longest_runs_test(str_data, c, 8)
                        if longest_run_result:
                            self.pass_tests()
                        else:
                            self.fail_tests()
                    else:
                        self.fail_tests()
                else:
                    self.fail_tests()
            else:
                self.fail_tests()

    def run_test_suite(self, block_size: int):
        """
        This method runs all of the tests included in the NIST test suite for randomness
        :param block_size: the size of the blocks to look at
        """
        for c in self.bin.columns:
            print("\t", Colours.Bold + "Running tests for", c + Colours.End)
            passed_values, p_values, str_data = [], [], self.bin.bin_data[c]

            passed, p_val = self.monobit_test(str_data, c)
            passed_values.append(passed)
            p_values.append(p_val)

            passed, p_val = self.block_frequency_test(str_data, c, block_size)
            passed_values.append(passed)
            p_values.append(p_val)

            passed, p_val = self.runs_test(str_data, c)
            passed_values.append(passed)
            p_values.append(p_val)

            passed, p_val = self.longest_runs_test(str_data, c, 8)
            passed_values.append(passed)
            p_values.append(p_val)

            passed, p_val = self.longest_runs_test(str_data, c, 128)
            passed_values.append(passed)
            p_values.append(p_val)

            passed, p_val = self.longest_runs_test(str_data, c, 10000)
            passed_values.append(passed)
            p_values.append(p_val)

            if False in passed_values:
                self.fail_tests()
            else:
                self.pass_tests()

    def fail_tests(self):
        print("\t", Colours.Bold + "Failing all subsequent tests" + Colours.End)

    def pass_tests(self):
        print("\t", Colours.Bold + "Passed all randomness tests" + Colours.End)

    def monobit_test(self, str_data: str, column: str):
        """
        **From the NIST documentation**
        The focus of this test is the proportion of zeros and ones for the entire sequence. The purpose of this test is
        to determine whether the number of ones and zeros in a sequence are approximately the same as would be expected
        for a truly random sequence. This test assesses the closeness of the fraction of ones to 1/2, that is the number
        of ones and zeros ina  sequence should be about the same. All subsequent tests depend on this test.
        :param str_data: this is the bit string being tested.
        :return: True | False if the test passed or failed
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
        return self.print_result("Monobit Test", column, p_val), p_val

    def test_monobit_test(self):
        """
        This is a test method for the monobit test method based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Testing Monobit Test" + Colours.End)
        results, p_val = self.monobit_test(self.test_data, "Test Data")
        if (p_val - 0.109599) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)

    def block_frequency_test(self, str_data: str, column: str, block_size: int):
        """
        **From the NIST documentation**
        The focus of this tests is the proportion of ones within M-bit blocks. The purpose of this tests is to determine
        whether the frequency of ones in an M-bit block is approximately M/2, as would be expected under an assumption
        of randomness. For block size M=1, this test degenerates to the monobit frequency test.
        :param str_data: this is the bit string being tested.
        :param column: this is the name of the bit string being tested.
        :param block_size: the size of the blocks that the binary sequence is partitioned into
        :return: True | False if the test passed or failed
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
        p_val = spc.gammaincc(num_blocks / 2, stat / 2)
        return self.print_result("Block Frequency Test", column, p_val), p_val

    def test_block_frequency_test(self):
        """
        This is a test method for the block frequency test method based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Testing Block Frequency Test" + Colours.End)
        results, p_val = self.block_frequency_test(self.test_data, "Test Data", 3)
        if (p_val - 0.706438) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)

    def runs_test(self, str_data: str, column: str):
        """
        **From the NIST documentation**
        The focus of this tests if the total number of runs in the sequences, where a run is an uninterrupted sequence
        of identical bits. A run of length k consists of k identical bits and is bounded before and after with a bit of
        the opposite value. The purpose of the runs tests is to determine whether the number of runs of ones and zeros
        of various lengths is as expected for a random sequence. In particular, this tests determines whether the
        oscillation between zeros and ones is either too fast or too slow.
        :param str_data: this is the bit string being tested.
        :param column: this is the name of the bit string being tested.
        :return: True | False if the test passed or failed
        """
        ones_count, n = 0, len(str_data)
        for char in str_data:
            if char == '1':
                ones_count += 1
        proportion, vobs = float(ones_count / n), 1
        for i in range(n - 1):
            if str_data[i] != str_data[i + 1]:
                vobs += 1
        num = (vobs - (2 * n * proportion * (1 - proportion)))
        den = (2 * math.sqrt(2 * n) * proportion * (1 - proportion))
        p_val = spc.erfc(num/den)
        return self.print_result("Runs Test", column, p_val), p_val

    def test_runs_test(self):
        """
        This is a test method for the runs test method based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Testing Runs Test" + Colours.End)
        results, p_val = self.runs_test(self.test_data, "Test Data")
        if (p_val - 0.500798) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)

    def longest_runs_test(self,  str_data: str, column: str, block_size: int):
        """
        This method calls the longest_run_test method with different parameters as per the NIST documentation
        :param str_data: this is the bit string being tested.
        :param column: this is the name of the bit string being tested.
        :param block_size: the size of the blocks that the binary sequence is partitioned into
        :return: True | False if the test passed or failed
        """
        if block_size == 8:
            m, k, piks = 3, 16, [0.2148, 0.3672, 0.2305, 0.1875]
            return self.longest_run_test(str_data, column, piks, m, k, block_size)
        elif block_size == 128:
            m, k, piks = 5, 49, [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
            return self.longest_run_test(str_data, column, piks, m, k, block_size)
        elif block_size == 10000:
            m, k, piks = 6, 75, [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
            return self.longest_run_test(str_data, column, piks, m, k, block_size)
        else:
            print("Unsupported block size, defaulting to 128-bits")
            m, k, piks = 5, 49, [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
            return self.longest_run_test(str_data, column, piks, m, k, block_size)

    def longest_run_test(self, str_data: str, column: str, pik_values: list, m: int, k: int, block_size: int):
        """
        **From the NIST documentation**
        The focus of the tests is the longest run of ones within M-bit blocks. The purpose of this tests is to determine
        whether the length of the longest run of ones within the tested sequences is consistent with the length of the
        longest run of ones that would be expected in a random sequence. Note that an irregularity in the expected
        length of the longest run of ones implies that there is also an irregularity ub tge expected length of the long
        est run of zeroes. Therefore, only one test is necessary for this statistical tests of randomness
        :param str_data: this is the bit string being tested.
        :param column: this is the name of the bit string being tested.
        :return: True | False if the test passed or failed
        """
        # Check if there is enough data to run the test
        if len(str_data) > block_size:
            # Work out the number of blocks, discard the remainder
            # pik = [0.2148, 0.3672, 0.2305, 0.1875]
            num_blocks = int(len(str_data) / block_size)
            block_start, block_end = 0, block_size
            frequencies = numpy.zeros(m + 1)
            for i in range(num_blocks):
                # Slice the binary string into a block
                block_data = str_data[block_start:block_end]
                # Keep track of the number of ones
                max_run_count, run_count = 0, 0
                if block_data[0] == '1':
                    run_count += 1
                for i in range(1, block_size):
                    if block_data[i] == '1':
                        run_count += 1
                        max_run_count = max(max_run_count, run_count)
                    else:
                        max_run_count = max(max_run_count, run_count)
                        run_count = 0
                run_length = min(max_run_count - 1, m)
                frequencies[run_length] += 1
                block_start += block_size
                block_end += block_size
            chi_squared = 0
            for i in range(len(frequencies)):
                chi_squared += (pow(frequencies[i] - (k * pik_values[i]), 2.0))/(k * pik_values[i])
            p_val = spc.gammaincc(float(3/2), float(chi_squared/2))
            return self.print_result("Longest Run Test " + str(block_size) + " bits", column, p_val), p_val
        else:
            return self.print_result("Longest Run Test " + str(block_size) + " bits", column, 0.0), 0.0

    def test_longest_runs_test(self):
        """
        This is a test method for the longest run test method based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Testing Longest Run Test" + Colours.End)
        results, p_val = self.longest_runs_test(self.test_data_8, "Test Data", 8)
        if (p_val - 0.180609) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)

    def get_binary_matrix_rank(self, m, q):
        """

        :return:
        """
        print(lng.matrix_rank(m))


if __name__ == '__main__':
    rng_tester = RandomnessTester(None)
    rng_tester.test_monobit_test()
    rng_tester.test_block_frequency_test()
    rng_tester.test_runs_test()
    rng_tester.test_longest_runs_test()

    matrix = numpy.matrix([[0, 1, 0], [1, 1, 0], [0, 1, 0]])
    rng_tester.get_binary_matrix_rank(matrix, 3)

    matrix = numpy.matrix([[0, 1, 0], [1, 0, 1], [0, 1, 1]])
    rng_tester.get_binary_matrix_rank(matrix, 3)