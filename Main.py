__author__ = 'x433165'

import numpy
import pandas
import bitstring
import scipy.stats as sst
import scipy.fftpack as sff
import scipy.special as spc
from functools import reduce


def sumi(x):
    return 2 * x - 1


def su(x, y):
    return x + y


def sus(x):
    return (x - 0.5) ** 2


def sq(x):
    return int(x) ** 2


def logo(x):
    return x * numpy.log(x)


def get_binary_returns():
    dataframe = pandas.read_csv("C:\\Users\\x433165\\Documents\\Random Number Generators\\Market Data\\SP500.csv")
    returns = numpy.array(dataframe["Return"])

    binary_returns = ""
    for r in returns:
        bin_r = bitstring.BitArray(float=r, length=64)
        binary_returns += bin_r._getbin()

    return binary_returns


def monobitfrequencytest(binin):
    ss = [int(el) for el in binin]
    sc = map(sumi, ss)
    sn = reduce(su, sc)
    sobs = numpy.abs(sn) / numpy.sqrt(len(binin))
    pval = spc.erfc(sobs / numpy.sqrt(2))
    return pval


if __name__ == '__main__':
    binret = get_binary_returns()
    print(monobitfrequencytest(binret))
