# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 19:14:19 2020

@author: bosch

"""
N = 512
bits = 8

# Create input sequence  (for -128 to +127)
input_values = [-118] * N

# Initialize internal state of DAC
sum1 = 0

output_values = []
test_point = []

for sample in input_values:

    # synchronous operations
    sum1_d = sum1

    # asynchronous operations
    if sum1_d > 0:
        out = 1
        fb = 2**(bits - 1) - 1
    else:
        out = 0
        fb = -2**(bits - 1)

    delta = sample - fb
    sum1 = delta + sum1_d

    output_values.append(out)
    test_point.append(sum1)
