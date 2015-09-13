### Introduction
----------------

r4nd0m is a project created by Stuart Reid to test the validity of the random walk hypothesis by subjecting discretized market returns to the NIST suite of cryptographic tests for randomness. This project contains standalone (static) implementations of each of the NIST tests as well as various methods and classes for downloading market data, and converting that data to a binary representation.

### Dependencies
----------------

Each test in the suite may or may not depend on one or all of the below packages. To be extra safe, you could just import everything.

1. **scipy.fftpack** as fft - fast fourier transform pack for the spectral test
2. **scipy.stats** as sst - general statistical functions used in the tests
3. **scipy.special** as spc - special functions for P-value computations
4. **math** - general mathematical functions used in the tests
5. **numpy** - for general data processing and array manipulation
6. **pandas** - dataframes be converted to binary using BinaryFrame
7. **Quandl** - for interfacing with the Quandl.com API to download data
8. **bitstring** - for converting floating point numbers to binary (not recommended)
9. other dependencies include **os** and **copy**

### Contributors
----------------

1. [Stuart Reid](http://www.TuringFinance.com) see [Hacking The Random Walk Hypothesis](http://www.TuringFinance.com/hacking-the-random-walk-hypothesis)

### Project Stucture
--------------------

The whole project is broken up into six classes and a main script which pulls everything together. Each class contains standalone code for performing one or more of the functions required to actually apply the NIST suite to historical market returns. The classes in the project include:

1. **r4nd0m** - this is the main script which pulls everything together.
3. **RandomnessTester** - this class contains all of the NIST tests.
4. **BinaryMatrix** - this class encapsulates the algorithm specified in the NIST documentation for calculating the rank of a binary matrix. This is not the same as the SVD method used to compute the rank of a matrix which is why the scipy.linalg package couldn't be used.
5. **BinaryFrame** - this class, as the name suggests, is just a way of converting a pandas DataFrame to a dictionary of lists of binary strings (samples) with the same column names. This dictionary and the decimal to binary conversion methods are encapsulated in this class. RandomnessTester simply takes in a BinaryFrame object and applies all of the NIST tests to the binary strings in the dictionary.
6. **QuandlInterface** and **Argument** - these two classes work together to allow you to interface with the Quandl.com API and download and join lists of datasets. Interesting dataset lists can be found in the MetaData folder of the project and your personal Quandl authentication token can be stored in a .private.csv local file and loaded at runtime.
7. **Colours** - this class just makes things look cool in the console.

The UML diagram below shows how the project is structured (constructed using Dia):

![UML diagram](https://github.com/StuartGordonReid/r4nd0m/blob/master/Diagrams/r4nd0m%20architecture.png)

### Binary Conversion Methodology
---------------------------------

Muliple binary conversion methodologies are supported by the BinaryFrame class, but the only one which appears to not introduce bias into the binary strings is discretization. Should you choose to make use to the BinaryFrame object, it takes in a pandas DataFrame and returns a BinaryFrame which encapsulates a dictionary of lists of binary strings. The column names from the DataFrame are used as the keys to the dictionary, to retrieving the list of binary strings is quite easy. Each element in the list represents a sample of the full binary string which was generated from the column data in the DataFrame.


### Example Usage for each Test
-------------------------------

The below "tutorial" shows how to very simply just apply each test in the suite to a binary strings. This tutorial does not deal with any of the automated methods for running the full suite of tests on a BinaryFrame object because most people would most probably not need to use all of the tests and would probably prefer some freedom regarding how they interface with the NIST randomness tests.

## Step 1 - Create a Randomness Tester Object

```python
rng_tester = RandomnessTester(None, False, 00, 00)
```


