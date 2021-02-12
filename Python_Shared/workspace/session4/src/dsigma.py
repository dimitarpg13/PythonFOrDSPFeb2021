# -*- coding: utf-8 -*-
"""
Delta Sigma Model (Simple List Version)
10/10/2020
@author: Dan Boschen
"""


def ds_list(input_values, input_width, total_samps=500):
    '''
    2nd order Delta Sigmna model (list version)

    Dan Boschen 10/11/2020

    Parameters
    ----------

    input_values: list of ints, or single int
        Digital sample values vs time (for a single int will maintain constant
        output for total_samps)

    input_width: positive integer
        Bit width of input

    total_samps: positive integer, optional
        (default =500) total number of samples to use for single integer input.

    Returns
    -------

    output_values: list of ints, values 0 or 1
        Output analog values vs time

    To-Do
    -------
    - Convert to a generator
    - Convert to the more efficient EAFP error trapping style
    - Allow any iterable input containing integers
    - Parametize accumulator bit widths and saturate on overflow
    - Allow for debug case returning all internal states
    - Implement with fixed point data type


    '''

    # allowing for list or integer input (Showing LBYL Style)
    if isinstance(input_values, int):
        input_values = [input_values] * total_samps

    elif not isinstance(input_values, list):
        raise TypeError("Input must be list of integers or literal int")

    elif not all([isinstance(i, int) for i in input_values]):
        raise TypeError("Input must be list of integers or literal int")

    # initialization
    sum1 = 0
    sum2 = 0
    out_values = []

    # create output by iterating through input_values
    for sample in input_values:

        # compute next state (clock update)
        sum1d = sum1
        sum2d = sum2

        # asynchronous operations
        if sum2d < 0:
            out = 0
            fb = -2**(input_width - 1)
            fbx2 = 2 * fb
        else:
            out = 1
            fb = 2**(input_width - 1) - 1
            fbx2 = 2 * fb + 1

        delta1 = sample - fb
        delta2 = sum1d - fbx2

        sum1 = sum1d + delta1
        sum2 = sum2d + delta2

        # mapping to any output scale (here 0 and 1)
        out_values.append(out)
        # end for

    return out_values


# %% Tests


if (__name__ == "__main__"):

    import csv

    # Demonstrating a simplified test with a single vector of input_values:
    # Test function result with input that matches results stored in
    # ds_data.txt
    input_values = [28] * 500 + [-2**20] * 1000

    out = ds_list(input_values, 24)

    # insert errors to confirm error handling
    # out[200:205] = [99] * 5

    results = zip(input_values, out)     # results is an iterator

    def strip_header(reader):
        for row in reader:
            if row[0].startswith('#'):
                continue
            yield row

    with open("../data/ds_data.txt") as f:

        reader = csv.reader(f, delimiter=',')
        fail = 0    # count failures
        err = ""    # for error message

        for count, row in enumerate(strip_header(reader)):

            # apply int() to each item in row
            # from file, return as tuple of (in,out) to
            # match results
            data = tuple(map(int, row))
            result = next(results)      # get next result from simulation

            if (data != result):
                fail += 1
                # new f-string debug feature in py 3.8:
                print(f"{data = }")
                print(f"{result = }")
                print(f"Results don't match at row {count+1}")
                prompt = input("Continue? Y/N [enter] ")
                if (prompt.upper() == "N"):
                    err = ", user terminated"
                    break
    if fail:
        print(f"{count+1} values compared, # of errs = {fail}{err}")
    else:
        print(f"Success all values matched, {count+1} values compared")
