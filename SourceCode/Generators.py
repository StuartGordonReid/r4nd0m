import random as sys_random
import numpy.random as numpy_random
from Crypto.Random import random as crypto_random


class Generators:
    def __init__(self, length):
        self.length = length

    def numpy_float(self):
        return numpy_random.uniform(low=0.0, high=1.0, size=self.length)

    def numpy_integer(self):
        return numpy_random.randint(low=-250, high=250, size=self.length)

    def system_integer(self, low=-250, high=250):
        rng = sys_random.SystemRandom()
        nrng = []
        for x in range(self.length):
            nrng.append(rng.randint(low, high))
        return nrng

    def crypto_integer(self, low=-250, high=250):
        nrng = []
        for x in range(self.length):
            nrng.append(crypto_random.randint(low, high))
        return nrng