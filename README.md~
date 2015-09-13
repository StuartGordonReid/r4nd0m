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

## Create a Randomness Tester Object

To create a RandomnessTester object which can be used independently of the BinaryFrame approach just pass in a None reference for the BinaryFrame object.

```python
rng_tester = RandomnessTester(None)
```

To test that the RandomnessTester is working correctly (i.e. check that the computed P-values for each example data sets in the TestData folder match the expected P-values) do the following

```python
rng_tester.test_randomness_tester()
```

The expected output from this method is given below:

```
	 Testing Monobit Test
	 pi          	p expected =  0.578211 	p computed = 0.578211
	 e           	p expected =  0.953749 	p computed = 0.953749
	 sqrt2       	p expected =  0.811881 	p computed = 0.811881
	 sqrt3       	p expected =  0.610051 	p computed = 0.610051

	 Testing Block Frequency Test
	 pi          	p expected =  0.380615 	p computed = 0.380615
	 e           	p expected =  0.211072 	p computed = 0.211072
	 sqrt2       	p expected =  0.833222 	p computed = 0.833222
	 sqrt3       	p expected =  0.473961 	p computed = 0.473961

	 Testing Independent Runs Test
	 pi          	p expected =  0.419268 	p computed = 0.419268
	 e           	p expected =  0.561917 	p computed = 0.561917
	 sqrt2       	p expected =  0.313427 	p computed = 0.313427
	 sqrt3       	p expected =  0.261123 	p computed = 0.261123

	 Testing Longest Runs Test
	 pi          	p expected =  0.02439 	p computed = 0.024390
	 e           	p expected =  0.718945 	p computed = 0.718945
	 sqrt2       	p expected =  0.012117 	p computed = 0.012117
	 sqrt3       	p expected =  0.446726 	p computed = 0.446726

	 Check Spectral Test
	 pi          	p expected =  0.010186 	p computed = 0.010186
	 e           	p expected =  0.847187 	p computed = 0.847187
	 sqrt2       	p expected =  0.581909 	p computed = 0.581909
	 sqrt3       	p expected =  0.776046 	p computed = 0.776046

	 Check Non Overlapping Patterns Test
	 pi          	p expected =  0.165757 	p computed = 0.165757
	 e           	p expected =  0.07879 	p computed = 0.078790
	 sqrt2       	p expected =  0.569461 	p computed = 0.569461
	 sqrt3       	p expected =  0.532235 	p computed = 0.532235

	 Check Overlapping Patterns Test
	 pi          	p expected =  0.296897 	p computed = 0.296897
	 e           	p expected =  0.110434 	p computed = 0.110434
	 sqrt2       	p expected =  0.791982 	p computed = 0.791982
	 sqrt3       	p expected =  0.082716 	p computed = 0.082716

	 Check Universal Test
	 pi          	p expected =  0.669012 	p computed = 0.669012
	 e           	p expected =  0.282568 	p computed = 0.282568
	 sqrt2       	p expected =  0.130805 	p computed = 0.130805
	 sqrt3       	p expected =  0.165981 	p computed = 0.165981

	 Check Serial Test
	 pi          	p expected =  0.143005 	p computed = 0.143005
	 e           	p expected =  0.766182 	p computed = 0.766182
	 sqrt2       	p expected =  0.861925 	p computed = 0.861925
	 sqrt3       	p expected =  0.1575 	p computed = 0.157500

	 Check Approximate Entropy Test
	 pi          	p expected =  0.361595 	p computed = 0.361595
	 e           	p expected =  0.700073 	p computed = 0.700073
	 sqrt2       	p expected =  0.88474 	p computed = 0.884740
	 sqrt3       	p expected =  0.180481 	p computed = 0.180481

	 Check Cumulative Sums Test
	 pi          	p expected =  0.628308 	p computed = 0.628308
	 e           	p expected =  0.669887 	p computed = 0.669886
	 sqrt2       	p expected =  0.879009 	p computed = 0.879009
	 sqrt3       	p expected =  0.917121 	p computed = 0.917121

	 Random Excursions Test
	 pi          	p expected =  0.844143 	p computed = 0.844143
	 e           	p expected =  0.786868 	p computed = 0.786868
	 sqrt2       	p expected =  0.216235 	p computed = 0.216235
	 sqrt3       	p expected =  0.783283 	p computed = 0.783283

	 Random Excursions Variant Test
	 pi          	p expected =  0.760966 	p computed = 0.760966
	 e           	p expected =  0.826009 	p computed = 0.826009
	 sqrt2       	p expected =  0.566118 	p computed = 0.566118
	 sqrt3       	p expected =  0.155066 	p computed = 0.155066

	 Testing Matrix Rank Test
	 This may take a while please be patient.
	 pi          	p expected =  0.083553 	p computed = 0.083553
	 e           	p expected =  0.306156 	p computed = 0.306156
	 sqrt2       	p expected =  0.82381 	p computed = 0.823810
	 sqrt3       	p expected =  0.314498 	p computed = 0.314498

	 Check Linear Complexity Test
	 This may take a while please be patient.
	 pi          	p expected =  0.255475 	p computed = 0.255475
	 e           	p expected =  0.826335 	p computed = 0.826335
	 sqrt2       	p expected =  0.317127 	p computed = 0.317127
	 sqrt3       	p expected =  0.346469 	p computed = 0.346469
```


