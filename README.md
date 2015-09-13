### Introduction
----------------

r4nd0m is a project created by Stuart Reid to test the validity of the random walk hypothesis by subjecting discretized market returns to the NIST suite of cryptographic tests for randomness. This project contains standalone (static) implementations of each of the NIST tests as well as various methods and classes for downloading market data, and converting that data to a binary representation.

### Disclaimer
--------------

r4nd0m implements the NIST suite of Cryptographic tests in Python and carries the same disclaimer as the original [C implementation](http://csrc.nist.gov/groups/ST/toolkit/rng/documentation_software.html). Software disclaimer: "This software was developed by Stuart Reid. Stuart Reid assumes no responsibility whatsoever for its use by other parties, and makes no guarantees, expressed or implied, about its quality, readibility, or any other characteristic. Usage of this implementation should acknowledge this repository, and the original NIST implementation."

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

#### Create a Randomness Tester Object

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

#### Apply the Monobit test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the proportion of zeros and ones for the entire sequence. The purpose of this test is
to determine whether the number of ones and zeros in a sequence are approximately the same as would be expected
for a truly random sequence. This test assesses the closeness of the fraction of ones to 1/2, that is the number
of ones and zeros ina  sequence should be about the same. All subsequent tests depend on this test.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.monobit(example_binary_string)
```

#### Apply the Block Frequency test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this tests is the proportion of ones within M-bit blocks. The purpose of this tests is to determine
whether the frequency of ones in an M-bit block is approximately M/2, as would be expected under an assumption
of randomness. For block size M=1, this test degenerates to the monobit frequency test.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.block_frequency(example_binary_string, block_size=64)
```

The block_size parameter tells the method how big each substring (block) of the data should be.

#### Apply the Independent Runs test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this tests if the total number of runs in the sequences, where a run is an uninterrupted sequence
of identical bits. A run of length k consists of k identical bits and is bounded before and after with a bit of
the opposite value. The purpose of the runs tests is to determine whether the number of runs of ones and zeros
of various lengths is as expected for a random sequence. In particular, this tests determines whether the
oscillation between zeros and ones is either too fast or too slow.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.independent_runs(example_binary_string)
```

#### Apply the Longest Run of Ones test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of the tests is the longest run of ones within M-bit blocks. The purpose of this tests is to determine
whether the length of the longest run of ones within the tested sequences is consistent with the length of the
longest run of ones that would be expected in a random sequence. Note that an irregularity in the expected
length of the longest run of ones implies that there is also an irregularity ub tge expected length of the long
est run of zeroes. Therefore, only one test is necessary for this statistical tests of randomness

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.longest_runs(example_binary_string)
```

#### Apply the Matrix Rank Transformation test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of the test is the rank of disjoint sub-matrices of the entire sequence. The purpose of this test is
to check for linear dependence among fixed length sub strings of the original sequence. Note that this test
also appears in the DIEHARD battery of tests.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.matrix_rank(example_binary_string, matrix_size=16)
```

The matrix_size parameter tells the method how big each matrix which is constructed from the data should be. A number 4 would result in 4x4 matrices and a number 16 would result in 16x16 matrices etc. Note that this test **depends** on the BinaryMatrix class contained inside the RandomnessTester.py file.

#### Apply the Spectral (Discrete Fourier Transform) test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the peak heights in the Discrete Fourier Transform of the sequence. The purpose of
this test is to detect periodic features (i.e., repetitive patterns that are near each other) in the tested
sequence that would indicate a deviation from the assumption of randomness. The intention is to detect whether
the number of peaks exceeding the 95 % threshold is significantly different than 5 %.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.spectral(example_binary_string)
```

#### Apply the Non Overlapping Patterns test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the number of occurrences of pre-specified target strings. The purpose of this
test is to detect generators that produce too many occurrences of a given non-periodic (aperiodic) pattern.
For this test and for the Overlapping Template Matching test of Section 2.8, an m-bit window is used to
search for a specific m-bit pattern. If the pattern is not found, the window slides one bit position. If the
pattern is found, the window is reset to the bit after the found pattern, and the search resumes.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.non_overlapping_patterns(example_binary_string, pattern="000000001", num_blocks=8)
```

The pattern parameter tells the method what binary pattern it should match on, and the num_block parameter tells the method how many blocks it should create from the data. These blocks do not overlap with one another which is why this is called the non overlapping patterns test.

#### Apply the Overlapping Patterns test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of the Overlapping Template Matching test is the number of occurrences of pre-specified target
strings. Both this test and the Non-overlapping Template Matching test of Section 2.7 use an m-bit
window to search for a specific m-bit pattern. As with the test in Section 2.7, if the pattern is not found,
the window slides one bit position. The difference between this test and the test in Section 2.7 is that
when the pattern is found, the window slides only one bit before resuming the search.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.non_overlapping_patterns(example_binary_string, pattern_size=9, block_size=1032)
```

The pattern parameter tells the method what binary pattern it should match on, and the block_size parameter tells the method how many big each blog created from the data should be. These blocks do overlap with one another which is why this is called the overlapping patterns test.

#### Apply the Universal test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the number of bits between matching patterns (a measure that is related to the
length of a compressed sequence). The purpose of the test is to detect whether or not the sequence can be
significantly compressed without loss of information. A significantly compressible sequence is considered
to be non-random. **This test is always skipped because the requirements on the lengths of the binary
strings are too high i.e. there have not been enough trading days to meet the requirements.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.universal(example_binary_string)
```

NOTE: the universal test requires quite a lot of data to produce a statistically significant result.

#### Apply the Linear Complexity test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the length of a linear feedback shift register (LFSR). The purpose of this test is to
determine whether or not the sequence is complex enough to be considered random. Random sequences are
characterized by longer LFSRs. An LFSR that is too short implies non-randomness.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.linear_complexity(example_binary_string, block_size=500)
```

The block size parameter specifies how bit each block (partition of the binary string data) should be. It is recommended that a block size of greater than or equal to 500 bits is used. Note also that the Linear Complexity test uses the berlekamp massey algorithm which has been implemented in the RandomnessTester.py file.

#### Apply the Serial test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the frequency of all possible overlapping m-bit patterns across the entire
sequence. The purpose of this test is to determine whether the number of occurrences of the 2m m-bit
overlapping patterns is approximately the same as would be expected for a random sequence. Random
sequences have uniformity; that is, every m-bit pattern has the same chance of appearing as every other
m-bit pattern. Note that for m = 1, the Serial test is equivalent to the Frequency test of Section 2.1.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.linear_complexity(example_binary_string, pattern_length=16, method="both")
```

The pattern_length parameter specifies how long the patterns which are matched should be. Note that this test returns two P-values if the method parameter is set to "both", the first P-value if the method parameter is set to "first", and the minimum of the two P-values if the method parameter is set to "min".

#### Apply the Approximate Entropy test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

As with the Serial test of Section 2.11, the focus of this test is the frequency of all possible overlapping
m-bit patterns across the entire sequence. The purpose of the test is to compare the frequency of overlapping
blocks of two consecutive/adjacent lengths (m and m+1) against the expected result for a random sequence.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.approximate_entropy(example_binary_string, pattern_length=16)
```

The pattern_length parameter specifies how long the patterns which are matched should be.

#### Apply the Cumulative Sums test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the maximal excursion (from zero) of the random walk defined by the cumulative sum of
adjusted (-1, +1) digits in the sequence. The purpose of the test is to determine whether the cumulative sum of
the partial sequences occurring in the tested sequence is too large or too small relative to the expected
behavior of that cumulative sum for random sequences. This cumulative sum may be considered as a random walk.
For a random sequence, the excursions of the random walk should be near zero. For certain types of non-random
sequences, the excursions of this random walk from zero will be large.

```python
example_binary_string = "01010101010101010101010101010101"
p_value = rng_tester.cumulative_sums(example_binary_string, method="forward")
```

There are two methods for performing the cumulative sums test: forwards and backwards. When the method parameter is equal to "backward", the input data is reversed and the cumulative sums test is applied as if the method passed was "forward".

#### Apply the Random Excursions test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the number of cycles having exactly K visits in a cumulative sum random walk. The
cumulative sum random walk is derived from partial sums after the (0,1) sequence is transferred to the
appropriate (-1, +1) sequence. A cycle of a random walk consists of a sequence of steps of unit length taken at
random that begin at and return to the origin. The purpose of this test is to determine if the number of visits
to a particular state within a cycle deviates from what one would expect for a random sequence. This test is
actually a series of eight tests (and conclusions), one test and conclusion for each of the states:

States -> -4, -3, -2, -1 and +1, +2, +3, +4.

```python
example_binary_string = "01010101010101010101010101010101"
p_values = rng_tester.random_excursions(example_binary_string)
```

Note that this test returns 8 P-values in the form of a numpy array. This is the P-value associated with each state.

#### Apply the Random Excursions Variant test to one binary string sample

Note that this description is taken from [the NIST documentation](http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf)

The focus of this test is the total number of times that a particular state is visited (i.e., occurs) in a
cumulative sum random walk. The purpose of this test is to detect deviations from the expected number of visits
to various states in the random walk. This test is actually a series of eighteen tests (and conclusions), one
test and conclusion for each of the states: -9, -8, …, -1 and +1, +2, …, +9.

```python
example_binary_string = "01010101010101010101010101010101"
p_values = rng_tester.random_excursions_variant(example_binary_string)
```

Note that this test returns 18 P-values in the form of a numpy array. This is the P-value associated with each state. Note also that this test makes use of the get_frequency method included in the RandomnessTester.py file.




