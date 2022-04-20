from functools import reduce


class MultipleAccumulate:
    data_list: list
    accumulate_functions = []

    def __init__(self, data_list, *args):
        self.data_list = data_list
        for arg in args:
            self.accumulate_functions.append(arg)

    def get_data(self):
        res = {}
        for ifun in self.accumulate_functions:
            res[ifun.__name__] = reduce(ifun, self.data_list)
        return res
