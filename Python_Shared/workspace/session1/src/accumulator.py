# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:53:05 2021

@author: bosch
"""
# %%  This is cell 1
N = 512
bits = 8

# Create the input sequence.
input_values = [50] * N

# Iniitialize the internal state.
sum1 = 0

# %% This is cell 2
# Create the output by iterating through the input values.
dac_out = []
for sample in input_values:
    # Complete all synchronous operations first:
    sum1_d = sum1

    # Ccomplete all asynchronous operations
    sum1 = sample + sum1_d

    # DAC
    dac = 3 / 2 ** bits

    # update output
    dac_out.append(dac * sum1_d)


