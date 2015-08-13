import scipy.special as spc
import numpy.linalg as lng
import numpy
import math


class Colours:
    """
    Just used to make the standard-out a little bit less ugly
    """
    Pass, Fail, End, Bold, Info, Italics = '\033[92m', '\033[91m', '\033[0m', '\033[1m', '\033[94m', '\x1B[3m'


class RandomnessTester:
    def __init__(self, bin, method, real_data, start_year, end_year, block_size):
        """
        Initializes a randomness tester object for testing binary sequences for randomness
        :param bin: this is a "BinaryFrame" object which is a conversion of a pandas DataFrame into a binary dictionary
        """
        self.method = method
        self.real_data = real_data
        self.start_year = start_year
        self.end_year = end_year
        self.block_size = block_size

        self.bin = bin
        self.condition = 0.001
        self.epsilon = 0.00000000001
        self.test_data = "11001001000011111101101010100010001000010110100011" \
                         "00001000110100110001001100011001100010100010111000"
        self.test_data_8 = "11001100000101010110110001001100111000000000001001" \
                           "00110101010001000100111101011010000000110101111100" \
                           "1100111001101101100010110010"
        self.test_data_rank = "01011001001010101101"

    def get_string(self, p_val):
        if p_val >= 0:
            if p_val < self.condition:
                return Colours.Fail + "{0:.5f}".format(p_val) + "\t" + Colours.End
            else:
                return Colours.Pass + "{0:.5f}".format(p_val) + "\t" + Colours.End
        else:
            return "{0:.4f}".format(p_val) + "\t" + Colours.End

    def get_aggregate_pval(self, pvals):
        bin_counts = numpy.zeros(10)
        for p in pvals:
            pos = min(int(math.floor(p * 10)), 9)
            bin_counts[pos] += 1
        chi_squared = 0
        expected_count = len(pvals) / 10
        for bin_count in bin_counts:
            chi_squared += pow(bin_count - expected_count, 2.0) / expected_count
        return spc.gammaincc(9.0/2.0, chi_squared/2.0)

    def get_aggregate_pass(self, pvals):
        npvals = numpy.array(pvals)
        return (npvals > self.condition).sum() / len(pvals)

    def print_dates(self, blocks):
        if self.real_data and self.method == "discretize":
            filler = "".zfill(64)
            string_out = filler.replace("0", " ")
            step = (self.end_year - self.start_year) / blocks
            dates = numpy.arange(start=self.start_year, stop=self.end_year, step=step)
            for i in range(blocks):
                start_string = str(int(dates[i]))
                string_out += start_string + "\t"
            print(string_out)

    def run_test_suite(self, block_size, q_size):
        """
        This method runs all of the tests included in the NIST test suite for randomness
        :param block_size: the size of the blocks to look at
        """
        for c in self.bin.columns:
            print(Colours.Bold + "\n\tRunning " + self.bin.method + " based tests on", c + Colours.End, "\n")
            binary_strings = self.bin.bin_data[c]

            test_names = ["\tMonobit Test Results",
                          "\tBlock Frequency Test",
                          "\tIndependent Runs Test",
                          "\tLongest Runs Test",
                          "\tMatrix Rank Test"]

            pvals = [[], [], [], [], []]

            for i in range(len(test_names)):
                length = len(test_names[i])
                space = 40 - length
                filler = "".zfill(space)
                filler = filler.replace("0", " ")
                test_names[i] += filler

            pval_strings = ["", "", "", "", ""]
            for i in range(len(binary_strings)):
                passed_values, p_values, str_data = [], [], binary_strings[i]

                p_val = self.monobit_test(str_data)
                pval_strings[0] += self.get_string(p_val)
                pvals[0].append(p_val)

                p_val = self.block_frequency_test(str_data, block_size)
                pval_strings[1] += self.get_string(p_val)
                pvals[1].append(p_val)

                p_val = self.runs_test(str_data)
                pval_strings[2] += self.get_string(p_val)
                pvals[2].append(p_val)

                p_val = self.longest_runs_test(str_data)
                pval_strings[3] += self.get_string(p_val)
                pvals[3].append(p_val)

                p_val = self.binary_matrix_rank_test(str_data, q_size)
                pval_strings[4] += self.get_string(p_val)
                pvals[4].append(p_val)

            aggregate_pvals, aggregate_pass = [], []
            for i in range(len(binary_strings)):
                aggregate_pvals.append(self.get_aggregate_pval(pvals[0]))
                aggregate_pass.append(self.get_aggregate_pass(pvals[0]))

                aggregate_pvals.append(self.get_aggregate_pval(pvals[1]))
                aggregate_pass.append(self.get_aggregate_pass(pvals[1]))

                aggregate_pvals.append(self.get_aggregate_pval(pvals[2]))
                aggregate_pass.append(self.get_aggregate_pass(pvals[2]))

                aggregate_pvals.append(self.get_aggregate_pval(pvals[3]))
                aggregate_pass.append(self.get_aggregate_pass(pvals[3]))

                aggregate_pvals.append(self.get_aggregate_pval(pvals[4]))
                aggregate_pass.append(self.get_aggregate_pass(pvals[4]))

            self.print_dates(len(binary_strings))
            for i in range(len(test_names)):
                pass_string = Colours.Bold + Colours.Fail + "FAIL!\t" + Colours.End
                if aggregate_pass[i] >= 0.96:
                    pass_string = Colours.Bold + Colours.Pass + "PASS!\t" + Colours.End
                if (numpy.array(pvals[i]) == -1.0).sum() > 0:
                    pass_string = Colours.Bold + "SKIP!\t" + Colours.End

                pval_string = Colours.Bold + Colours.Fail + "p=" + "{0:.5f}".format(aggregate_pvals[i]) + "\t" + Colours.End
                if aggregate_pvals[i] > self.condition:
                    pval_string = Colours.Bold + Colours.Pass + "p=" + "{0:.5f}".format(aggregate_pvals[i]) + "\t" + Colours.End
                if (numpy.array(pvals[i]) == -1.0).sum() > 0:
                    pval_string = "p=SKIPPED\t"

                print(test_names[i] + pass_string + pval_string + pval_strings[i])

    def fail_tests(self):
        print("\t", Colours.Bold + "Failed to pass all randomness tests" + Colours.End)

    def pass_tests(self):
        print("\t", Colours.Bold + "Passed all randomness tests" + Colours.End)

    def zeros_and_ones_count(self, str_data: str):
        ones, zeros = 0, 0
        # If the char is 0 minus 1, else add 1
        for char in str_data:
            if char == '0':
                zeros += 1
            else:
                ones += 1
        print("\t", Colours.Italics + "Count 1 =", ones, "Count 0 =", zeros, Colours.End)

    def monobit_test(self, str_data: str):
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
        return p_val

    def test_monobit_test(self):
        """
        This is a test method for the monobit test method based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Testing Monobit Test" + Colours.End)
        p_val = self.monobit_test(self.test_data)
        if (p_val - 0.109599) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)

    def block_frequency_test(self, str_data: str, block_size: int):
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
        num_blocks = math.floor(len(str_data) / block_size)
        block_start, block_end = 0, block_size
        # Keep track of the proportion of ones per block
        proportion_sum = 0.0
        for i in range(num_blocks):
            # Slice the binary string into a block
            block_data = str_data[block_start:block_end]
            # Keep track of the number of ones
            ones_count = 0
            for char in block_data:
                if char == '1':
                    ones_count += 1
            pi = ones_count / block_size
            proportion_sum += pow(pi - 0.5, 2.0)
            # Update the slice locations
            block_start += block_size
            block_end += block_size
        # Calculate the p-value
        chi_squared = 4.0 * block_size * proportion_sum
        p_val = spc.gammaincc(num_blocks / 2, chi_squared / 2)
        return p_val

    def test_block_frequency_test(self):
        """
        This is a test method for the block frequency test method based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Testing Block Frequency Test" + Colours.End)
        p_val = self.block_frequency_test(self.test_data, 3)
        if (p_val - 0.706438) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)

    def runs_test(self, str_data: str):
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
        p, vobs = float(ones_count / n), 1
        tau = 2 / math.sqrt(len(str_data))
        if abs(p - 0.5) > tau:
            return 0.0
        else:
            for i in range(1, n):
                if str_data[i] != str_data[i-1]:
                    vobs += 1
            # expected_runs = 1 + 2 * (n - 1) * 0.5 * 0.5
            # print("\t", Colours.Italics + "Observed runs =", vobs, "Expected runs", expected_runs, Colours.End)
            num = abs(vobs - 2.0 * n * p * (1.0 - p))
            den = 2.0 * math.sqrt(2.0 * n) * p * (1.0 - p)
            p_val = spc.erfc(float(num/den))
            return p_val

    def test_runs_test(self):
        """
        This is a test method for the runs test method based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Testing Runs Test" + Colours.End)
        p_val = self.runs_test(self.test_data)
        if (p_val - 0.500798) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)

    def longest_runs_test(self, str_data: str):
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
        if len(str_data) < 128:
            print("\t", "Not enough data to run test!")
            return 0.0 < self.condition, 0.0
        elif len(str_data) < 6272:
            k, m = 3, 8
            v_values = [1, 2, 3, 4]
            pik_values = [0.21484375, 0.3671875, 0.23046875, 0.1875]
        elif len(str_data) < 75000:
            k, m = 5, 128
            v_values = [4, 5, 6, 7, 8, 9]
            pik_values = [0.1174035788, 0.242955959, 0.249363483, 0.17517706, 0.102701071, 0.112398847]
        else:
            k, m = 6, 10000
            v_values = [10, 11, 12, 13, 14, 15, 16]
            pik_values = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

        # Work out the number of blocks, discard the remainder
        # pik = [0.2148, 0.3672, 0.2305, 0.1875]
        num_blocks = math.floor(len(str_data) / m)
        frequencies = numpy.zeros(k + 1)
        block_start, block_end = 0, m
        for i in range(num_blocks):
            # Slice the binary string into a block
            block_data = str_data[block_start:block_end]
            # Keep track of the number of ones
            max_run_count, run_count = 0, 0
            for j in range(0, m):
                if block_data[j] == '1':
                    run_count += 1
                    max_run_count = max(max_run_count, run_count)
                else:
                    max_run_count = max(max_run_count, run_count)
                    run_count = 0
            if max_run_count < v_values[0]:
                frequencies[0] += 1
            for j in range(k):
                if max_run_count == v_values[j]:
                    frequencies[j] += 1
            if max_run_count > v_values[k-1]:
                frequencies[k] += 1
            block_start += m
            block_end += m
        # print(frequencies)
        chi_squared = 0
        for i in range(len(frequencies)):
            chi_squared += (pow(frequencies[i] - (num_blocks * pik_values[i]), 2.0))/(num_blocks * pik_values[i])
        p_val = spc.gammaincc(float(k/2), float(chi_squared/2))
        return p_val

    def test_longest_runs_test(self):
        """
        This is a test method for the longest run test method based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Testing Longest Run Test" + Colours.End)
        p_val = self.longest_runs_test(self.test_data_8)
        if (p_val - 0.180609) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)

    def binary_matrix_rank_test(self, str_data: str, q: int):
        """
        **From the NIST documentation**
        The focus of the test is the rank of disjoint sub-matrices of the entire sequence. The purpose of this test is
        to check for linear dependence among fixed length sub strings of the original sequence. Note that this test
        also appears in the DIEHARD battery of tests [7].
        """
        shape = (q, q)
        n = len(str_data)
        block_size = q * q
        block_start, block_end = 0, block_size
        num_m = math.floor(n / (q * q))
        if num_m > 0:
            max_ranks = [0, 0, 0]
            for im in range(num_m):
                block_data = str_data[block_start:block_end]
                block = numpy.zeros(len(block_data))
                for i in range(len(block_data)):
                    if block_data[i] == '1':
                        block[i] = 1.0
                m = block.reshape(shape)
                rank = lng.matrix_rank(m)
                if rank == q:
                    max_ranks[0] += 1
                elif rank == (q - 1):
                    max_ranks[1] += 1
                else:
                    max_ranks[2] += 1
                # Update index trackers
                block_start += block_size
                block_end += block_size
            chi = 0.0
            piks = [0.2888, 0.5776, 0.1336]
            for i in range(len(piks)):
                chi += pow((max_ranks[i] - (piks[i] * num_m)), 2.0) / (piks[i] * num_m)
            p_val = math.exp(-chi/2)
            return p_val
        else:
            return -1.0

    def test_binary_matrix_rank_test(self):
        """
        This is a test method for the binary matrix rank test based on the example in the NIST documentation
        """
        print(Colours.Bold + "\n\t Binary Matrix Rank Test" + Colours.End)
        p_val = self.binary_matrix_rank_test(self.test_data_rank, 3)
        if (p_val - 0.741948) < self.epsilon:
            print("\t", Colours.Pass + Colours.Bold + "Passed Unit Test" + Colours.End)
        else:
            print("\t", Colours.Fail + Colours.Bold + "Failed Unit Test" + Colours.End)


if __name__ == '__main__':
    rng_tester = RandomnessTester(None)
    rng_tester.test_monobit_test()
    rng_tester.test_block_frequency_test()
    rng_tester.test_runs_test()
    rng_tester.test_longest_runs_test()
    rng_tester.test_binary_matrix_rank_test()
