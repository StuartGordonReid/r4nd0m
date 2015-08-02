__author__ = 'x433165'


from DataDownloader import QuandlInterface, Argument
from RandomnessTests import RandomnessTester
from BinaryFrame import BinaryFrame
import pandas
import numpy
from Crypto import Random as crand


def construct_binary_frame(method):
    token = ""
    try:
        private = pandas.read_csv(".private.csv")
        token = private["Token"][0]
    except FileNotFoundError:
        print("No private settings found")
    downloader = QuandlInterface(token)
    data_sets = ["SBK"]
    data_prefix = "GOOG/JSE_"
    transform = "rdiff"
    start_date = "2010-01-01"
    end_date = "2015-01-01"
    my_arguments = []
    for ds in data_sets:
        my_arguments.append(Argument(ds, start_date, end_date, data_prefix, None, transform))
    data_frame_full = downloader.get_data_sets(my_arguments)
    if method == "convert":
        binary_frame = BinaryFrame(data_frame_full)
        binary_frame.convert_754()
        return binary_frame
    elif method == "discretize":
        binary_frame = BinaryFrame(data_frame_full)
        binary_frame.discretize()
        return binary_frame


if __name__ == '__main__':
    prng = numpy.random.uniform(low=-1.0, high=1.0, size=80000)
    '''
    prng_list = []
    for i in range(80000):
        r = crand.get_random_bytes(10)
        prng_list.append(float(r/1000000))
    '''
    prng_data = pandas.DataFrame(numpy.array(prng))
    prng_data.columns = ["PRNG"]
    prng_binary_frame = BinaryFrame(prng_data)
    prng_binary_frame.convert_int()

    rng_tester = RandomnessTester(prng_binary_frame)
    rng_tester.mono_bit_test()

    my_binary_frame = construct_binary_frame("convert")
    rng_tester = RandomnessTester(my_binary_frame)
    rng_tester.mono_bit_test()

    my_binary_frame = construct_binary_frame("discretize")
    rng_tester = RandomnessTester(my_binary_frame)
    rng_tester.mono_bit_test()
