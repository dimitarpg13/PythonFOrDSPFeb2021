# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 09:45:51 2020

Simple script of a first order Delta Sigma DAC to demonstrate Spyder

@author: Dan
"""
N = 512             # number of samples
bits = 8           # number of bits

# Create the input sequence.
input_values = [-127] * N

# Initialize internal state of DAC and output result list.
# States update at stat of each iteration, so initialization is to be the
# input values of each register.
sum1 = 0
output_values = []
test_point = []

# Create output by iterating through input_values.
for sample in input_values:

    # Compute next state.
    sum1_d = sum1

    # Comlete asynchronous operations (asynchronous = outputs that change
    # directly in response to inputs).
    out = 1 if sum1_d > 0 else 0
    fb = -2**(bits - 1) + out * (2**bits - 1)
    delta = sample - fb
    sum1 = sum1_d + delta

    # Update output and test_point
    output_values.append(out)
    test_point.append(sum1)
