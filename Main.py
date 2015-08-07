from DataDownloader import QuandlInterface, Argument
from RandomnessTests import RandomnessTester
from BinaryFrame import BinaryFrame
import pandas
import numpy
import math
import csv
import os
import random


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
        binary_frame.convert_unbiased()
        return binary_frame
    elif method == "discretize":
        binary_frame = BinaryFrame(data_frame_full)
        binary_frame.discretize()
        return binary_frame


def get_strong_random_sequence(length):
    rng = random.SystemRandom()
    nrng = numpy.empty(length)
    for x in range(length):
        nrng[x] = rng.random() * 2.0 - 1.0
    return nrng


if __name__ == '__main__':
    print("\nTesting Mersenne Twister Using Unbiased Converter\n")
    # prng = numpy.random.uniform(low=-1.0, high=1.0, size=80000)
    prng = get_strong_random_sequence(80000)
    prng_data = pandas.DataFrame(numpy.array(prng))
    prng_data.columns = ["Mersenne"]
    prng_binary_frame = BinaryFrame(prng_data)
    prng_binary_frame.convert_unbiased()
    rng_tester = RandomnessTester(prng_binary_frame)
    rng_tester.run_test_suite(6400)

    print("\nTesting Mersenne Twister Using Discretization\n")
    prng_binary_frame = BinaryFrame(prng_data)
    prng_binary_frame.discretize()
    rng_tester = RandomnessTester(prng_binary_frame)
    rng_tester.run_test_suite(100)

    print("\nTesting Deterministic Sequence Using Unbiased Converter\n")
    nrand = numpy.empty(80000)
    for i in range(80000):
        nrand[i] = (i % 10) / 10
    nrand -= numpy.mean(nrand)
    nrand_data = pandas.DataFrame(numpy.array(nrand))
    nrand_data.columns = ["Deterministic"]
    nrand_binary_frame = BinaryFrame(nrand_data)
    nrand_binary_frame.convert_unbiased()
    rng_tester = RandomnessTester(nrand_binary_frame)
    rng_tester.run_test_suite(6400)

    print("\nTesting Deterministic Sequence Using Discretization\n")
    nrand_binary_frame = BinaryFrame(nrand_data)
    nrand_binary_frame.discretize()
    rng_tester = RandomnessTester(nrand_binary_frame)
    rng_tester.run_test_suite(100)

    print("\nTesting Market Data Using Unbiased Converter\n")
    t = setup_environment()
    my_binary_frame = construct_binary_frame("convert", t)
    rng_tester = RandomnessTester(my_binary_frame)
    rng_tester.run_test_suite(6400)

    print("\nTesting Market Data Using Discretization\n")
    my_binary_frame = construct_binary_frame("discretize", t)
    rng_tester = RandomnessTester(my_binary_frame)
    rng_tester.run_test_suite(100)
