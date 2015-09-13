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
5. **BinaryFrame** - this class, as the name suggests, is just a way of converting a pandas DataFrame to a dictionary of binary strings with the same column names. This dictionary and the decimal to binary conversion methods are encapsulated in this class. RandomnessTester simply takes in a BinaryFrame object and applies all of the NIST tests to the binary strings in the dictionary.
6. **QuandlInterface** and **Argument** - these two classes work together to allow you to interface with the Quandl.com API and download and join lists of datasets. Interesting dataset lists can be found in the MetaData folder of the project and your personal Quandl authentication token can be stored in a .private.csv local file and loaded at runtime.
7. **Colours** - this class just makes things look cool in the console.

The UML diagram below shows how the project is structured (constructed using Dia):

![UML diagram](https://github.com/StuartGordonReid/r4nd0m/blob/master/Diagrams/r4nd0m%20architecture.png)

### Binary Conversion Methodologies
-----------------------------------

Two binary conversion methodologies are supported by the project. 

##### Discretization 

This method simply loops through the floating point data in the market data pandas DataFrame and converts it to binary by testing if the return is greater than, or less than, 0. If the return is greater than 0, the return is represented as a 1-bit whereas if the return is less than 0 it is represented as a 0-bit. In the special case that the return is exactly equal to 0, the return is represented as 01 which removes the otherwise small bias towards producing zero-bits.

##### Adapted IEEE 754 Converter

This method loops over the floating point returns data in the market data pandas DataFrame and converts it using the standard IEEE 754 method of converting floating point numbers to binary. This is done using the bitstring package. The problem with this is that the conversion is biased in two ways, firstly, because numbers are only differentiated by one sign bit but are are otherwise equivalent and, secondly, because zero is represented as a sequence of zeros which results in a bias towards zero bits. For example,

+-0.0 = 00000000000000000000000000000000<br />
-0.25 = 10111110100000000000000000000000<br />
+0.25 = 00111110100000000000000000000000

To overcome this if the floating point number was negative, the bits (excluding) the sign bit are flipped and any and all floating points equal to zero are replaced with an unbiased bitstring of alternating zeros and ones,

+-0.0 = 01010101010101010101010101010101<br />
-0.25 = 10111110100000000000000000000000<br />
+0.25 = 01000001011111111111111111111111

Assuming the floating point numbers are uniformly distributed between -1.0 and 1.0, this methodology results in an expectation that the number of ones and zeros in the resulting bitstring should be approximately equal. This is the condition under which the NIST tests for randomness should be applied. *Note: there may be other, yet undiscovered, challenges with this methodology*

### NIST Tests for Randomness
-----------------------------
