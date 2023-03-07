import itertools


class Factor:
    def __init__(self, variables, default=0):
        self.variables = variables
        keys = [tuple(sorted(zip(self.variables.keys(), r)))
                for r in itertools.product(*self.variables.values())]
        self.f = dict(zip(keys, [default]*len(keys)))

    def __getitem__(self, e):
        return self.f[tuple(sorted(self._filter_inputs(e).items()))]

    def __setitem__(self, e, x):
        k = tuple(sorted(self._filter_inputs(e).items()))
        if k in self.f:
            self.f[k] = x
        else:
            raise KeyError(e)

    def _filter_inputs(self, e):
        return dict([(k, v) for k, v in e.items() if k in self.variables])

    def inputs(self):
        return [dict(a) for a in self.f.keys()]

    def values(self):
        return [a for a in self.f.values()]


def observe(factor, variable, value):
    """
    Function that restricts a variable to some value in a given factor.
    :param factor:
    :param variable:
    :param value:
    :return:
    """


def multiply(factor1, factor2):
    """
    Function that multiplies two factors
    :param factor1:
    :param factor2:
    :return:
    """


def sumout(factor, variable):
    """
    Function that sums out a variable in a given factor.
    :param factor:
    :param variable:
    :return:
    """


def normalize(factor):
    """
    Function that normalizes a factor by dividing each entry by the sum of all the entries.
    This is useful when the factor is a distribution (i.e. sum of the probabilities must be 1).
    :param factor:
    :return:
    """


def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
    """
    function that computes Pr(queryVariables|evidenceList) by variable elimination. This function
    should restrict the factors in factorList according to the evidence in evidenceList.
    Next, it should sum-out the hidden variables from the product of the factors in factorList.
    The variables should be summed out in the order given in orderedListOfHiddenVariables.
    Finally, the answer can be normalized if a probability distribution that sums up to 1 is desired.
    :param factorList:
    :param queryVariables:
    :param orderedListOfHiddenVariables:
    :param evidenceList:
    :return:
    """