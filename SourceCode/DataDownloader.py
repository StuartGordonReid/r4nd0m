import os
import Quandl
import pandas


class QuandlInterface:
    def __init__(self, api_key):
        """
        An interface for downloading data from Quandl
        :param api_key: [YOUR API KEY] (taken from the .private.csv file)
        """
        self.api_key = api_key

    def get_data_set(self, argument):
        file_name = argument.to_string()
        basepath = os.path.dirname(__file__)
        path = os.path.abspath(os.path.join(basepath, os.pardir, "MarketData", file_name))
        try:
            data_frame = pandas.read_csv(path)
            data_frame = data_frame.set_index("Date")
            return data_frame
        except:
            data_frame = self.download_data_set(argument)
            data_frame.to_csv(path, mode="w+")
            return data_frame

    def download_data_set(self, argument):
        """
        This method tries to fetch a data set from Quandl
        :param argument: an argument object which contains the information to construct the request
        :return: a pandas DataFrame containing the data
        """
        assert isinstance(argument, Argument)
        data_frame = None
        try:
            data_set_name = argument.id
            if argument.prefix is not None:
                data_set_name = argument.prefix + data_set_name
            data_frame = Quandl.get(data_set_name, authtoken=self.api_key,
                                    trim_start=argument.start, trim_end=argument.end,
                                    transformation=argument.transformation, collapse=argument.collapse)
            assert isinstance(data_frame, pandas.DataFrame)
            for d in argument.drop:
                try:
                    data_frame = data_frame.drop(d, axis=1)
                except:
                    continue
        except Quandl.DatasetNotFound:
            print("Data set not found")
        except Quandl.ErrorDownloading:
            print("Error downloading")
        except Quandl.ParsingError:
            print("Parsing error")
        except Quandl.WrongFormat:
            print("Wrong format")
        except Quandl.CallLimitExceeded:
            print("Call limit exceeded")
        except Quandl.CodeFormatError:
            print("Code format error")
        except Quandl.MissingToken:
            print("Missing token")
        if data_frame is None:
            raise Exception("Data Set Not Initialized", argument.id)
        else:
            return data_frame

    def get_data_sets(self, arguments):
        """
        This method just calls the get_data_set() method to download and join various data sets
        :param arguments: a list of Argument objects
        :return: a pandas DataFrame
        """
        # assert isinstance(arguments, [Argument])
        combined_data_frame = None
        for arg in arguments:
            assert isinstance(arg, Argument)
            arg_data_frame = self.get_data_set(arg)
            new_columns = []
            for i in range(len(arg_data_frame.columns)):
                new_columns.append(arg.id + "_" + arg_data_frame.columns[i])
            arg_data_frame.columns = new_columns
            if combined_data_frame is None:
                combined_data_frame = arg_data_frame
            else:
                combined_data_frame = combined_data_frame.join(arg_data_frame)
        combined_data_frame = combined_data_frame.dropna()
        return combined_data_frame


class Argument:
    def __init__(self, id, start, end, prefix=None, drop=None, rdiff="none", collapse="none"):
        """
        An Argument object which contains the information to construct a request to send to Quandl
        :param id: the id of the data set
        :param start: the start date
        :param end: the end date
        :param prefix: the database prefix
        :param drop: the columns to drop from the dataframe
        :param rdiff: the transformation to do (usually percentage change)
        :param collapse: the frequency of data to download
        :return:
        """
        self.id = id
        self.start = start
        self.end = end
        self.transformation = rdiff
        self.collapse = collapse
        self.prefix = prefix
        # The default drop columns for Google Finance data
        if drop is None:
            drop = ["High", "Low", "Open", "Volume", "Adjusted Close", ""]
        self.drop = drop

    def to_string(self):
        unique_id = "Cache"
        unique_id += " id=" + self.id
        unique_id += " start=" + self.start
        unique_id += " end=" + self.end
        unique_id += " trans=" + self.transformation
        unique_id += ".csv"
        return unique_id.replace("\\", "-").replace("/", "-")
