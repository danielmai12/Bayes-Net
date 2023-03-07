import itertools


class Factor:
    def __init__(self, variables, entries):
        """
        :param variables: list of variables (i.e., ['A', 'B'])
        :param entries: dictionary of values of entries. Note: 0 - false, 1 - true
                       (i.e., {(0, 0): 0.9, (0, 1): 0.1, (1, 0): 0.0002, (1, 1): 0.9998}
        Note: for single variable, each entry consists only 1 element (either true or false) as follow (1,), (0,)
        """

        self.variables = variables
        self.entries = entries

    def get_variables(self):
        return self.variables

    def get_entries(self):
        return self.entries

    def get_probability(self, entry):
        return self.entries[entry]

    def is_contain_var(self, var):
        return var in self.variables


def observe(factor, variable, value):
    """
    Function that restricts a variable to some value in a given factor.
    :param factor: factor object
    :param variable: single variable which needs to be restricted to - example: 'Y'
    :param value: its value (either 1 or 0)
    :return:
        new Factor after restriction
    """
    current_variables = factor.get_variables()
    remain_vars = []
    target_idx = 0
    for i in range(len(current_variables)):
        if current_variables[i] == variable:
            target_idx = i
        else:
            remain_vars.append(current_variables[i])

    remain_entries = {}
    for key in factor.get_entries().keys():
        if key[target_idx] == value:
            new_key = list(key)[:target_idx] + list(key)[target_idx+1:]
            new_key = tuple(new_key)
            remain_entries[new_key] = factor.get_probability(key)

    return Factor(remain_vars, remain_entries)


def sumout(factor, variable):
    """
    Function that sums out a variable in a given factor.
    :param factor: factor object
    :param variable: single variable - hidden variables which need to be sum out from the product - example: 'Y'
    :return:
        new Factor after sum out the hidden variables
    """
    current_variables = factor.get_variables()
    remain_vars = []
    target_idx = 0
    for i in range(len(current_variables)):
        if current_variables[i] == variable:
            target_idx = i
        else:
            remain_vars.append(current_variables[i])

    remain_values = {}
    for key in factor.get_entries().keys():
        new_key = tuple(list(key)[:target_idx] + list(key)[target_idx+1:])
        if new_key in remain_values.keys():
            remain_values[new_key] += factor.get_probability(key)
            remain_values[new_key] = round(remain_values[new_key], 3)
        else:
            remain_values[new_key] = factor.get_probability(key)

    return Factor(remain_vars, remain_values)


def multiply(factor1, factor2):
    """
    Function that multiplies two factors
    :param factor1: first factor object
    :param factor2: second factor object
    :return: new Factor with:
                - variables: the union of the sets of variables in the two factors
    """
    f1_vars = factor1.get_variables()
    f2_vars = factor2.get_variables()
    # Find the union of two lists
    # Not using set here because it can change the order of the variables
    new_vars = f1_vars.copy()
    for var_f2 in f2_vars:
        if var_f2 not in new_vars:
            new_vars.append(var_f2)

    new_entries = {}
    if f1_vars == f2_vars:  # Special case 1: f1 and f2 have the same sets of variables
        for key in factor1.get_entries().keys():
            new_entries[key] = factor1.get_probability(key) * factor2.get_probability(key)
    elif len(f1_vars) + len(f2_vars) == len(new_vars):  # Special case 2:  f1 and f2 have no variables in common
        for f1_key in factor1.get_entries().keys():
            for f2_key in factor2.get_entries().keys():
                new_key = f1_key + f2_key
                new_entries[new_key] = factor1.get_probability(f1_key) * factor2.get_probability(f2_key)
    else:  # Case 3: f1 and f2 have common variables
        # generate all permutations
        perms = list(itertools.product((0, 1), repeat=len(new_vars)))

        for entry in perms:
            # find f1_prob given value of each var
            f1_prob = factor1.get_probability(tuple(entry[0:len(f1_vars)]))

            # find f2_prop given value of each var
            f2_key = []
            for var in f2_vars:
                f2_key.append(entry[new_vars.index(var)])
            f2_prob = factor2.get_probability(tuple(f2_key))

            new_entries[tuple(entry)] = round(f1_prob * f2_prob, 3)

    return Factor(new_vars, new_entries)


def normalize(factor):
    """
    Function that normalizes a factor by dividing each entry by the sum of all the entries.
    This is useful when the factor is a distribution (i.e. sum of the probabilities must be 1).
    :param factor: factor Object
    :return: a normalized factor where all entries sum to 1.
    """
    sum_entries = 0
    new_entries = {}

    for entry in factor.get_entries().keys():
        sum_entries += factor.get_probability(entry)

    for entry in factor.get_entries().keys():
        new_entries[entry] = round(factor.get_probability(entry) / sum_entries, 3)

    return Factor(factor.get_variables(), new_entries)


def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
    """
    Function that computes Pr(queryVariables|evidenceList) by variable elimination. This function
    should restrict the factors in factorList according to the evidence in evidenceList.
    Next, it should sum-out the hidden variables from the product of the factors in factorList.
    The variables should be summed out in the order given in orderedListOfHiddenVariables.
    Finally, the answer can be normalized if a probability distribution that sums up to 1 is desired.
    :param factorList: list of factor object from given bayes network
    :param queryVariables: list of query variables
    :param orderedListOfHiddenVariables: list of ordered list of hidden layers
    :param evidenceList: list of evidence list, each element in a list is a list containing variable and its value
    :return:
            result of Pr(queryVariables|evidenceList)
    """

    # Step 1: For each evidence variable and for each factor that contains the evidence variable
    #         restrict the factor by assigning the observed value to the evidence variable.
    print("Factor list after observe step: ")
    restricted_factors = []
    for factor in factorList:
        curr_factor = factor
        for evidence in evidenceList:  # evidence[0] is the var, and evidence[1] is the value
            if curr_factor.is_contain_var(evidence[0]):
                curr_factor = observe(curr_factor, evidence[0], evidence[1])
        restricted_factors.append(curr_factor)
        print("variables: {} and entries: {}".format(curr_factor.get_variables(), curr_factor.get_entries()))

    # Step 2: Eliminate each hidden variable by multiplying all factors that contain that hidden layer
    #         and sum out the hidden layer from that factor
    for var in orderedListOfHiddenVariables:
        if var in queryVariables:
            continue

        # find the factors that contain the hidden variable
        factors_have_var = []
        for factor in restricted_factors:
            if var in factor.get_variables():
                factors_have_var.append(factor)

        if len(factors_have_var) == 1:  # we do not have to multiply any factors, sum out the hidden layer
            new_factor = sumout(factors_have_var[0], var)
            print("variables: {} and entries: {}".format(new_factor.get_variables(), new_factor.get_entries()))
            if factors_have_var[0] in restricted_factors:
                restricted_factors.remove(factors_have_var[0])
            restricted_factors.append(new_factor)

        if len(factors_have_var) > 1:  # multiply all the factors containing the hidden var and sum out the hidden var
            product = factors_have_var[0]
            if factors_have_var[0] in restricted_factors:
                restricted_factors.remove(factors_have_var[0])
            for i in range(len(factors_have_var) - 1):
                product = multiply(product, factors_have_var[i+1])
                if factors_have_var[i+1] in restricted_factors:
                    restricted_factors.remove(factors_have_var[i+1])

            new_factor = sumout(product, var)  # sum out the hidden layer
            restricted_factors.append(new_factor)

    # for testing purposes
    print("\nFactor list after elimination (multiply + sum out) step : ")
    for factor in restricted_factors:
        print("variables: {} and entries: {}".format(factor.get_variables(), factor.get_entries()))

    # Step 3: Multiplying the remaining factors
    temp_factors = restricted_factors.copy()
    product = temp_factors[0]
    if temp_factors[0] in restricted_factors:
        restricted_factors.remove(temp_factors[0])
    for i in range(len(temp_factors) - 1):
        product = multiply(product, temp_factors[i + 1])
        if temp_factors[i + 1] in restricted_factors:
            restricted_factors.remove(temp_factors[i + 1])
    restricted_factors.append(product)
    # for testing purposes
    print("\nFactor list after elimination (multiply + sum out) step : ")
    for factor in restricted_factors:
        print("variables: {} and entries: {}".format(factor.get_variables(), factor.get_entries()))

    # Step 4: Normalize the factor
    norm_factor = normalize(restricted_factors[0])
    print("\nNormalized factor variable: {} and entries: {}".format(norm_factor.get_variables(), norm_factor.get_entries()))

    return norm_factor
