from DataDownloader import QuandlInterface, Argument
from RandomnessTests import RandomnessTester
from BinaryFrame import BinaryFrame
import pandas
import numpy
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


def construct_binary_frame(method, token, stream_size):
    downloader = QuandlInterface(token)
    data_sets = ["INDEX_GSPC",
                 "FUND_NASDX",
                 "INDEX_SSEC",
                 "INDEX_N225"]
    data_prefix = "YAHOO/"
    transform = "rdiff"
    start_date = "2000-01-01"
    end_date = "2015-01-01"
    my_arguments = []
    for ds in data_sets:
        my_arguments.append(Argument(ds, start_date, end_date, data_prefix, None, transform))
    data_frame_full = downloader.get_data_sets(my_arguments)
    binary_frame = BinaryFrame(data_frame_full, stream_size)
    binary_frame.convert(method)
    return binary_frame


def construct_long_binary_frame(method, stream_size):
    data = pandas.read_csv("S&P 500 History.csv")
    assert isinstance(data, pandas.DataFrame)
    data = data.set_index("Date")
    data = data.drop("Close", axis=1)
    binary_frame = BinaryFrame(data, stream_size)
    binary_frame.convert(method)
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


def run_experiments(block_sizes, q_sizes, length, stream_length, methods):
    for method in methods:
        prng = numpy_random(length)
        prng_data = pandas.DataFrame(numpy.array(prng))
        prng_data.columns = ["Mersenne"]
        prng_binary_frame = BinaryFrame(prng_data, stream_length)
        prng_binary_frame.convert(method, convert=False)
        rng_tester = RandomnessTester(prng_binary_frame)
        rng_tester.run_test_suite(block_sizes, q_sizes)

        nrand = numpy.empty(length)
        for i in range(length):
            nrand[i] = (i % 10) / 10
        nrand -= numpy.mean(nrand)
        nrand_data = pandas.DataFrame(numpy.array(nrand))
        nrand_data.columns = ["Deterministic"]
        nrand_binary_frame = BinaryFrame(nrand_data, stream_length)
        nrand_binary_frame.convert(method)
        rng_tester = RandomnessTester(nrand_binary_frame)
        rng_tester.run_test_suite(block_sizes, q_sizes)

        # t = setup_environment()
        # my_binary_frame = construct_binary_frame("discretize", t)
        my_binary_frame = construct_long_binary_frame(method, stream_length)
        rng_tester = RandomnessTester(my_binary_frame)
        rng_tester.run_test_suite(block_sizes, q_sizes)


if __name__ == '__main__':
    # "discretize"
    # "convert basis point"
    # "convert floating point"
    m = ["discretize"]
    run_experiments(128, 32, (1024*2)*55, 1024*2, m)

