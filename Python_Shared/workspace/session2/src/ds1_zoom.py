# -*- coding: utf-8 -*-

N = 512
bits = 8

# Create input sequence
input_values = [-102] * N

# initialize internal state
sum1 = 0

output_values = []

test_point = []


# create output by iterating through the input values

for sample in input_values:

    # synchronous
    sum1_d = sum1

    # asynchronous

    if sum1_d >= 0:
        out = 1
        fb = 2**(bits - 1) - 1
    else:
        out = 0
        fb = -2**(bits - 1)

    delta = sample - fb
    sum1 = delta + sum1_d

    # update output and testpoint
    output_values.append(out)
    test_point.append(sum1)





