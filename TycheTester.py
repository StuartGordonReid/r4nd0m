import csv
import os
import random as sysrandom

import pandas
import numpy
from Crypto.Random import random

from SourceCode.DataDownloader import QuandlInterface, Argument
from SourceCode.RandomnessTests import RandomnessTester
from SourceCode.BinaryFrame import BinaryFrame


# TODO: Add better comments to this file
# TODO: Identify more markets to include in study
# TODO: Move Random Number Generators into Separate Class


def setup_environment():
    token = ""
    try:
        with open(".private.csv", "r") as csvfile:
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


def construct_binary_frame(data_sets, method, token, start, end, years_per_block):
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
    binary_frame.convert(method)
    return binary_frame


def construct_long_binary_frame(method, start, end, years_per_block):
    data = pandas.read_csv("MarketData\\.S&P500.csv")
    assert isinstance(data, pandas.DataFrame)
    data = data.set_index("Date")
    data = data.drop("Close", axis=1)
    data = data.reindex(index=data.index[::-1])
    binary_frame = BinaryFrame(data, start, end, years_per_block)
    binary_frame.convert(method)
    return binary_frame


def numpy_float_random(length):
    return numpy.random.uniform(low=0.0, high=1.0, size=length)


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


def run_experiments(data_sets, block_sizes, q_sizes, methods, start, end, years_per_block):
    breaker = "".zfill(200)
    breaker = breaker.replace('0', '*')
    for method in methods:
        print("\n" + breaker)
        print("METHOD =", method.upper())

        length = 256 * (end - start)
        prng = numpy_random(length)

        prng_data = pandas.DataFrame(numpy.array(prng))
        prng_data.columns = ["Mersenne"]
        prng_binary_frame = BinaryFrame(prng_data, start, end, years_per_block)
        prng_binary_frame.convert(method, convert=False)
        # method, real_data, start_year, end_year, block_size
        rng_tester = RandomnessTester(prng_binary_frame, method, False, 00, 00)
        rng_tester.run_test_suite(block_sizes, q_sizes)

        nrand = numpy.empty(length)
        for i in range(length):
            nrand[i] = (i % 10) / 10
        nrand -= numpy.mean(nrand)
        nrand_data = pandas.DataFrame(numpy.array(nrand))
        nrand_data.columns = ["Deterministic"]
        nrand_binary_frame = BinaryFrame(nrand_data, start, end, years_per_block)
        nrand_binary_frame.convert(method, convert=True)
        rng_tester = RandomnessTester(nrand_binary_frame, method, False, 00, 00)
        rng_tester.run_test_suite(block_sizes, q_sizes)

        t = setup_environment()
        my_binary_frame = construct_binary_frame(data_sets, method, t, start, end, years_per_block)
        rng_tester = RandomnessTester(my_binary_frame, method, True, start, end)
        # my_binary_frame = construct_long_binary_frame(method, stream_length)
        rng_tester.run_test_suite(block_sizes, q_sizes)
    print("\n" + breaker)


def clean_up():
    try:
        os.remove("authtoken.p")
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    m = ["discretize"]
    # , "convert basis point", "convert floating point"]
    run_experiments("MarketData\\.1900 plus.csv", 128, 16, m, 1900, 2015, 1.0)
    clean_up()
