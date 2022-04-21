from functools import reduce


class MultipleAccumulate:
    data_list: list
    accumulate_functions = []

    def __init__(self, data_list, *args):
        self.data_list = data_list
        i = 1
        for arg in args:
            print(arg)
            if arg.__name__ == '<lambda>':
                arg.__name__ = f'lambda{i}'
                i += 1
            self.accumulate_functions.append(arg)


    # nazwmac lamby nie przezywac
    def get_data(self):
        res = {}
        for ifun in self.accumulate_functions:
            print(ifun.__name__)
            res[ifun.__name__] = reduce(ifun, self.data_list)
        return res
