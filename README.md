# Tyche-Tester

Tyche is the Greek goddess of fortune and luck.

### Introduction
----------------

This project contains code which concerns itself with testing the random walk hypothesis using the NIST cryptographic suite of tests for randomness. This project includes an interface to Quandl which makes it especially easy to test various market data for randomness including, but not limited too, stock prices, interest rates, foreign exchange rates, and commodity prices.

### Project Stucture
--------------------

The project contains the following Python source files,

1. **Main.py** - this file contains example code which shows how to download market data, convert that market data into one or more binary representations which can be used in conjunction with the NIST test suite, and how to test that binary data for randomness.
2. **DataDownloader.py** - this file contain code for downloading market data from Quandl.com and joining it together to produce a complete pandas DataFrame of market data devoid of missing values which can then be converted into a BinaryFrame and tested for randomness.
3. **BinaryFrame.py** - this file contains methods for converting a pandas DataFrame into a so-called BinaryFrame. The BinaryFrame stores the column data from the DataFrame as binary strings in a dictionary. Two unbiased converters are supported. These are discussed in more detail in the binary converstion methodologies section of this readme file.
4. **RandomnessTests.py** - this file contains intuitive and easy to understand implementations of each of the randomness tests presented in the NIST test suite. These tests are discussed in a lot of detail in the NIST Tests for Randomness section of this readme file.

In addition to these, the project allows a user to create a local .private.csv file which contains private information such as one's Quandl authentication token and login details if you are using the project from behind a proxy. The file can be structured as follows:

### Binary Conversion Methodologies
-----------------------------------

### NIST Tests for Randomness
-----------------------------