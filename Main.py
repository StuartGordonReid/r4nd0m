__author__ = 'x433165'


from DataDownloader import QuandlInterface, Argument
from BinaryFrame import BinaryFrame
import pandas


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
        binary_frame.convert()
        return binary_frame
    elif method == "discretize":
        binary_frame = BinaryFrame(data_frame_full)
        binary_frame.discretize()
        return binary_frame


def mono_bit_test(bin):
    assert isinstance(bin, BinaryFrame)
    for c in bin.columns:
        str_data = bin.bin_data[c]
        count_zero = 0
        count_ones = 0
        for char in str_data:
            if char == '0':
                count_zero += 1
            else:
                count_ones += 1
        print(count_zero, count_ones)


if __name__ == '__main__':
    my_binary_frame = construct_binary_frame("convert")
    mono_bit_test(my_binary_frame)

    my_binary_frame = construct_binary_frame("discretize")
    mono_bit_test(my_binary_frame)
