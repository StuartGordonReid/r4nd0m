__author__ = 'x433165'

import os
import Quandl
import pandas


class QuandlInterface:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_data_set(self, argument):
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
                data_frame = data_frame.drop(d, axis=1)
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
            raise Exception("Data Set Not Initialized")
        else:
            return data_frame

    def get_data_sets(self, arguments):
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
        self.id = id
        self.start = start
        self.end = end
        self.transformation = rdiff
        self.collapse = collapse
        self.prefix = prefix
        if drop is None:
            drop = ["High", "Low", "Open", "Volume"]
        self.drop = drop
