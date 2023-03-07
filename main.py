from variable_elimination import *

# variables = ['X', 'Y', 'Z']
# values = {(1, 1, 1): 0.1, (1, 1, 0): 0.9, (1, 0, 1): 0.2, (1, 0, 0): 0.8,
#           (0, 1, 1): 0.4, (0, 1, 0): 0.6, (0, 0, 1): 0.3, (0, 0, 0): 0.7}
#
# f1 = Factor(variables, values)
#
#
# def test_observe():
#     f2 = observe(f1, 'X', 1)
#     print("f2_vars: {}".format(f2.get_variables()))  # f2_vars: ['Y', 'Z']
#     print("f2_values: {}".format(f2.get_entries()))  # f2_values: {(1, 1): 0.1, (1, 0): 0.9, (0, 1): 0.2, (0, 0): 0.8}
#
#     f3 = observe(f2, 'Z', 0)
#     print("f3_vars: {}".format(f3.get_variables()))  # f3_vars: ['Y']
#     print("f3_values: {}".format(f3.get_entries()))  # f3_values: {(1,): 0.9, (0,): 0.8}
#
#     f4 = observe(f3, 'Y', 0)
#     print("f3_vars: {}".format(f4.get_variables()))  # f3_vars: []
#     print("f3_values: {}".format(f4.get_entries()))  # f3_values: {(): 0.8}

# test_observe()

# variables = ['X', 'Y', 'Z']
# values = {(1, 1, 1): 0.03, (1, 1, 0): 0.07, (1, 0, 1): 0.54, (1, 0, 0): 0.36,
#           (0, 1, 1): 0.06, (0, 1, 0): 0.14, (0, 0, 1): 0.48, (0, 0, 0): 0.32}

# f_1 = Factor(variables, values)
#
# f_2 = sumout(f_1, 'Y')
# print("f2_vars: {}".format(f_2.get_variables()))  # f2_vars: ['Y', 'Z']
# print("f2_values: {}".format(f_2.get_entries()))  # f2_values: {(1, 1): 0.57, (1, 0): 0.43, (0, 1): 0.54, (0, 0): 0.46}


# variables_1 = ['X', 'Y']
# values_1 = {(1, 1): 0.1, (1, 0): 0.9, (0, 1): 0.2, (0, 0): 0.8}
# f_1 = Factor(variables_1, values_1)
#
# variables_2 = ['Y', 'Z']
# values_2 = {(1, 1): 0.3, (1, 0): 0.7, (0, 1): 0.6, (0, 0): 0.4}
# f_2 = Factor(variables_2, values_2)
#
# f_3 = multiply(f_1, f_2)
# print(f_3.get_entries())
#
# test_vars = ['Y']
# test_entry = {(0,): 0.2, (1,): 0.6}
# test_fac = Factor(test_vars, test_entry)
# ff = normalize(test_fac)
#
# print(ff.get_variables())
# print(ff.get_entries())

# Example:
"""
        E
        |
        v
        A -> W
        ^
        |
        B
Query: P(B| -a)?
"""

# Define factors
B_entries = {(1,): 0.3, (0,): 0.7}
B = Factor(['B'], B_entries)

E_entries = {(1,): 0.1, (0,): 0.9}
E = Factor(['E'], E_entries)

ABE_entries = {(1, 1, 1): 0.8, (1, 1, 0): 0.7, (1, 0, 1): 0.2, (1, 0, 0): 0.1,
               (0, 1, 1): 0.2, (0, 1, 0): 0.3, (0, 0, 1): 0.8, (0, 0, 0): 0.9}
A_B_E = Factor(['A', 'B', 'E'], ABE_entries)

WA_entries = {(1, 1): 0.8, (1, 0): 0.4, (0, 1): 0.2, (0, 0): 0.6}
W_A = Factor(['W', 'A'], WA_entries)

factorList = [B, E, A_B_E, W_A]
queryVariables = ['B']
orderedListOfHiddenVariables = ['W', 'E']
evidenceList = [['A', 0]]

result = inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)
# result should be {(1,): 0.123, (0,): 0.877} - means P(b|-a) = 0.123, P(-b|-a) = 0.877
