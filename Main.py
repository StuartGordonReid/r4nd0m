from DataDownloader import QuandlInterface, Argument
from RandomnessTests import RandomnessTester
from BinaryFrame import BinaryFrame
import pandas
import numpy
import math
import csv
import os
import random as sysrandom
from Crypto.Random import random


def setup_environment():
    token = ""
    try:
        with open('.private.csv', 'r') as csvfile:
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


def construct_binary_frame(method, token):
    downloader = QuandlInterface(token)
    data_sets = ["INDEX_GSPC", "FUND_NASDX", "INDEX_SSEC", "INDEX_N225"]
    data_prefix = "YAHOO/"
    transform = "rdiff"
    start_date = "2000-01-01"
    end_date = "2015-01-01"
    my_arguments = []
    for ds in data_sets:
        my_arguments.append(Argument(ds, start_date, end_date, data_prefix, None, transform))
    data_frame_full = downloader.get_data_sets(my_arguments)
    if method == "convert":
        binary_frame = BinaryFrame(data_frame_full)
        binary_frame.convert_basis_points_unbiased()
        return binary_frame
    elif method == "discretize":
        binary_frame = BinaryFrame(data_frame_full)
        binary_frame.discretize()
        return binary_frame


def construct_long_binary_frame(method):
    data = pandas.read_csv("S&P 500 History.csv")
    assert isinstance(data, pandas.DataFrame)
    data = data.set_index("Date")
    data = data.drop("Close", axis=1)
    if method == "convert":
        binary_frame = BinaryFrame(data)
        binary_frame.convert_basis_points_unbiased()
        return binary_frame
    elif method == "discretize":
        binary_frame = BinaryFrame(data)
        binary_frame.discretize()
        return binary_frame


def numpy_random(length):
    return numpy.random.randint(low=-250, high=250, size=length)


def system_random(length):
    rng = sysrandom.SystemRandom()
    nrng = []
    for x in range(length):
        nrng.append(rng.randint(-250, 250))
    return nrng


def crypto_random(length):
    nrng = []
    for x in range(length):
        nrng.append(random.randint(-250, 250))
    return nrng


def conversion_run(block_sizes, q_sizes):
    print("\nTesting Mersenne Twister")
    prng = crypto_random(80000)
    prng_data = pandas.DataFrame(numpy.array(prng))
    prng_data.columns = ["Mersenne"]
    prng_binary_frame = BinaryFrame(prng_data)
    prng_binary_frame.convert_basis_points_unbiased(convert=False)
    rng_tester = RandomnessTester(prng_binary_frame)
    rng_tester.run_test_suite(block_sizes, q_sizes)

    print("\nTesting Deterministic Sequence")
    nrand = numpy.empty(80000)
    for i in range(80000):
        nrand[i] = (i % 10) / 10
    nrand -= numpy.mean(nrand)
    nrand_data = pandas.DataFrame(numpy.array(nrand))
    nrand_data.columns = ["Deterministic"]
    nrand_binary_frame = BinaryFrame(nrand_data)
    nrand_binary_frame.convert_basis_points_unbiased()
    rng_tester = RandomnessTester(nrand_binary_frame)
    rng_tester.run_test_suite(block_sizes, q_sizes)

    print("\nTesting Market Data")
    t = setup_environment()
    # my_binary_frame = construct_binary_frame("convert", t)
    my_binary_frame = construct_long_binary_frame("convert")
    rng_tester = RandomnessTester(my_binary_frame)
    rng_tester.run_test_suite(block_sizes, q_sizes)


def discretize_run(block_sizes, q_sizes):
    print("\nTesting Mersenne Twister")
    prng = crypto_random(80000)
    prng_data = pandas.DataFrame(numpy.array(prng))
    prng_data.columns = ["Mersenne"]
    prng_binary_frame = BinaryFrame(prng_data)
    prng_binary_frame.discretize()
    rng_tester = RandomnessTester(prng_binary_frame)
    rng_tester.run_test_suite(block_sizes, q_sizes)

    print("\nTesting Deterministic Sequence")
    nrand = numpy.empty(80000)
    for i in range(80000):
        nrand[i] = (i % 10) / 10
    nrand -= numpy.mean(nrand)
    nrand_data = pandas.DataFrame(numpy.array(nrand))
    nrand_data.columns = ["Deterministic"]
    nrand_binary_frame = BinaryFrame(nrand_data)
    nrand_binary_frame.discretize()
    rng_tester = RandomnessTester(nrand_binary_frame)
    rng_tester.run_test_suite(block_sizes, q_sizes)

    print("\nTesting Market Data")
    t = setup_environment()
    # my_binary_frame = construct_binary_frame("discretize", t)
    my_binary_frame = construct_long_binary_frame("convert")
    rng_tester = RandomnessTester(my_binary_frame)
    rng_tester.run_test_suite(block_sizes, q_sizes)


if __name__ == '__main__':
    my_block_sizes = [8, 16, 64, 128, 256, 512, 1024]
    my_q_sizes = [2, 4, 8, 16, 32, 64]
    conversion_run(my_block_sizes, my_q_sizes)
    # discretize_run(my_block_sizes, my_q_sizes)

