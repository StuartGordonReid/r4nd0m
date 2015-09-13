import os
import csv
import numpy
import pandas

from SourceCode.Generators import Generators
from SourceCode.BinaryFrame import BinaryFrame
from SourceCode.RandomnessTests import RandomnessTester
from SourceCode.DataDownloader import QuandlInterface, Argument


def setup_environment():
    """
    This method just "sets up" your environment to run the program. It handles HTTP and HTTPS proxies and the Quandl
    authentication token. This information is read from a .private.csv file in the MetaData folder
    :return: the authentication token from Quandl
    """
    token = ""
    try:
        with open(os.path.join("MetaData", ".private.csv"), "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if row[0] == "HTTP" and row[1] != "None":
                    os.environ['HTTP_PROXY'] = row[1]
                if row[0] == "HTTPS" and row[1] != "None":
                    os.environ['HTTPS_PROXY'] = row[1]
                if row[0] == "Token" and row[1] != "None":
                    token = row[1]
    except FileNotFoundError:
        print("No private settings found")
    return token


def construct_binary_frame(data_sets, method, token, start, end, years_per_block, isamples):
    """
    This method is used to construct a BinaryFrame object from a meta-data file which specifies what data sets we want
    to download and what columns we are interested in from that data.
    :param data_sets: the file containing the data sets we want
    :param method: the method of conversion to binary
    :param token: a Quandl authentication token
    :param start: the start date
    :param end: the end date
    :param years_per_block: the time frame / dimension we want to look at
    :return: a BinaryFrame object which can work with the RandomnessTester class
    """
    downloader = QuandlInterface(token)
    data_file = pandas.read_csv(data_sets)
    data_sets = list(data_file["ID"])
    drop_columns = list(data_file["DROP"])
    data_prefix = ""
    transform = "rdiff"
    start_date = str(start) + "-01-01"
    end_date = str(end) + "-01-01"
    my_arguments = []
    for i in range(len(data_sets)):
        drop = drop_columns[i].split('#')
        if drop == "":
            drop = []
        my_arguments.append(Argument(data_sets[i], start_date, end_date, data_prefix, drop, transform))
    data_frame_full = downloader.get_data_sets(my_arguments)
    binary_frame = BinaryFrame(data_frame_full, start, end, years_per_block)
    binary_frame.convert(method, independent_samples=isamples)
    return binary_frame


def run_experiments(data_sets, block_sizes, q_sizes, method, start, end, years_per_block, isamples=False):
    """
    This method just runs the experiments which were used to write the blog post
    :param data_sets: the file containing a list of data sets we want
    :param block_sizes: a list of block sizes
    :param q_sizes: a list of matrix sizes
    :param start: the start date
    :param end: the end date
    :param methods: the methods of conversion to binary we want to test
    :param years_per_block: the time frame / dimension we want to look at
    :return: nothing just prints out stuff
    """
    print("\n")
    print("METHOD =", method.upper())

    length = 256 * (end - start)
    gen = Generators(length)
    prng = gen.numpy_integer()

    all_passed = []
    prng_data = pandas.DataFrame(numpy.array(prng))
    prng_data.columns = ["Mersenne"]
    prng_binary_frame = BinaryFrame(prng_data, start, end, years_per_block)
    prng_binary_frame.convert(method, convert=False, independent_samples=isamples)
    # method, real_data, start_year, end_year, block_size
    rng_tester = RandomnessTester(prng_binary_frame, False, 00, 00)
    passed = rng_tester.run_test_suite(block_sizes, q_sizes)
    for x in passed:
        all_passed.append(x)

    nrand = numpy.empty(length)
    for i in range(length):
        nrand[i] = (i % 10) / 10
    nrand -= numpy.mean(nrand)
    nrand_data = pandas.DataFrame(numpy.array(nrand))
    nrand_data.columns = ["Deterministic"]
    nrand_binary_frame = BinaryFrame(nrand_data, start, end, years_per_block)
    nrand_binary_frame.convert(method, convert=True, independent_samples=isamples)
    rng_tester = RandomnessTester(nrand_binary_frame, False, 00, 00)
    passed = rng_tester.run_test_suite(block_sizes, q_sizes)
    for x in passed:
        all_passed.append(x)

    t = setup_environment()
    my_binary_frame = construct_binary_frame(data_sets, method, t, start, end, years_per_block, isamples)
    rng_tester = RandomnessTester(my_binary_frame, True, start, end)
    passed = rng_tester.run_test_suite(block_sizes, q_sizes)
    for x in passed:
        all_passed.append(x)

    print("\n")
    return all_passed


def clean_up():
    """
    This just removes the Quandl authentication token pickle from the system
    :return: nothing
    """
    try:
        os.remove("authtoken.p")
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    m = "discretize"
    # "convert basis point"
    # "convert floating point"

    start_year, end_year = 1950, 2015
    file_name = "." + str(start_year) + " plus.csv"

    least_random_fit = 15
    least_random_interval = 1
    for interval in range(5, 6):
        path = os.path.join("MetaData", file_name)
        passed = run_experiments(path, 64, 4, m, start_year, end_year, interval)
        passed_avg = numpy.array(passed[2::]).mean()
        if passed_avg < least_random_fit:
            least_random_fit = passed_avg
            least_random_interval = interval
    print(least_random_interval, least_random_fit)
    clean_up()
