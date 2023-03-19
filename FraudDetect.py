from variable_elimination import *

""" 
T = travel, F = fraud, FP = foreign purchases, I = internet purchase, 
O = owns computer, C = computer-related purchase 
"""
travel_entries = {(0,): 0.95, (1,): 0.05}
T = Factor(['T'], travel_entries)

FT_entries = {(0, 0): 0.996, (0, 1): 0.99, (1, 0): 0.004, (1, 1): 0.01}
F_T = Factor(['F', 'T'], FT_entries)

FPFT_entries = {(0, 0, 0): 0.99, (0, 0, 1): 0.1, (0, 1, 0): 0.9, (0, 1, 1): 0.1,
                (1, 0, 0): 0.01, (1, 0, 1): 0.9, (1, 1, 0): 0.1, (1, 1, 1): 0.9}
FP_F_T = Factor(['FP', 'F', 'T'], FPFT_entries)

O_entries = {(0,): 0.3, (1,): 0.7}
O = Factor(['O'], O_entries)

IFO_entries = {(0, 0, 0): 0.999, (0, 0, 1): 0.99, (0, 1, 0): 0.989, (0, 1, 1): 0.98,
               (1, 0, 0): 0.001, (1, 0, 1): 0.01, (1, 1, 0): 0.011, (1, 1, 1): 0.02}
I_F_O = Factor(['I', 'F', 'O'], IFO_entries)

CO_entries = {(0, 0): 0.999, (0, 1): 0.9, (1, 0): 0.001, (1, 1): 0.1}
C_O = Factor(["C", "O"], CO_entries)

# Set up for inference
factor_list = [T, F_T, FP_F_T, O, I_F_O, C_O]
orderedListOfHiddenVariables = ["T", "FP", "F", "I", "O", "C"]

"""
What is the prior probability (i.e., before we search for previous computer related purchases and before we verify 
whether it is a foreign and/or an internet purchase) that the current transaction is a fraud?

Simplify question into query: P(F)?
"""
print("------------------------------------------ Evaluating P(F) -------------------------------------------------")
query_variables = ['F']
evidence_list = []
result = inference(factor_list, query_variables, orderedListOfHiddenVariables, evidence_list)

print("\nThe probability that the current transaction is Fraud (P(F)) is: ")
print("\t \t P(+f) = {}".format(result.get_probability((1,))))
print("\t \t P(-f) = {}".format(result.get_probability((0,))))

print("----------------------------------------------------------------------------------------------")

"""
What is the probability that the current transaction is a fraud once we have verified that it is a foreign transaction, 
but not an internet purchase and that the card holder purchased computer related accessories in the past week?

Simplify into query: P(F|+fp, -i, +c) 
"""
print("------------------------------ Evaluating P(F|+fp, -i, +c) -----------------------------------")

query_variables = ['F']
evidence_list = [['FP', 1], ['I', 0], ['C', 1]]
result = inference(factor_list, query_variables, orderedListOfHiddenVariables, evidence_list)

print("\nThe probability that the current transaction is Fraud (P(F|+fp, -i, +c)) is: ")
print("\t \t P(+f|+fp, -i, +c) = {}".format(result.get_probability((1,))))
print("\t \t P(-f|+fp, -i, +c) = {}".format(result.get_probability((0,))))

print("-----------------------------------------------------------------------------------------------")