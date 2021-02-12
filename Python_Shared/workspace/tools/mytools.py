"""
Custom Module with common tools

Copyright (C) 2018-2020 C. Daniel Boschen

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided
with the distribution.

3. The name of the author may not be used to endorse or promote
products derived from this software without specific prior
written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import itertools as it

# demonstrating importing a module global variable
x = 5

def disp(my_list, ncol = 4, width = 20):
    """
    Display list in column format, each successive item in list
    will be displayed in a separate column (increments by col
    first and then row)

    Dan Boschen 11/25/2019

    Parameters:
    -----------

    my_list:  List

    ncol: integer, optional
        number of columns, default = 4

    width: width, optional
        column spacing, default = 20

    Returns:
    --------
    None

    """
    def _abrev(name, width):
        if len(str(name)) > width-4:
            return str(name)[:width-4] + "..."
        else:
            return str(name)

    # ensure string and shorten all items to column width
    my_new_list = [_abrev(i, width) for i in my_list ]


    #create a format string for ncol columns spaced by width
    # result for width = 20 and ncol = 4 is
    # "{:<20}{:<20}{:<20}{:<20}"
    template = "".join(("{:<"+str(width)+"}") * ncol)

    #print using template
    for columns in  it.zip_longest(*[iter(my_new_list)] * ncol, fillvalue = ""):
        print(template.format(*columns))


def printmd(stringWithMarkdown):
    """
    Prints string with Markdown as an output of a code block
    """
    from IPython.display import Markdown, display
    display(Markdown(stringWithMarkdown))



# recursive memory profiler from
# https://code.tutsplus.com/tutorials/understand-how-much-memory-your-python-objects-use--cms-25609

from collections.abc import Mapping, Container        # updated to collections.abc CDB 10/19/2020
from sys import getsizeof


def deep_getsizeof(o, ids):
    """Find the memory footprint of a Python object

    This is a recursive function that drills down a Python object graph
    like a dictionary holding nested dictionaries with lists of lists
    and tuples and sets.

    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    really is.

    :param o: the object
    :param ids:
    :return:

    ex:
    x = '1234567'
    deep_getsizeof(x, set())
    44
    """
    d = deep_getsizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    # if isinstance(o, str) or isinstance(0, unicode):
    if isinstance(o, str):    # updated CDB 10/18/2020
        return r

    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())

    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)

    return r


def get_attributes(obj):
    # Returns all attributes excluding methods of an object and their values
    # as a dictionary
    # Dan Boschen 10/19/2020

    # Demorgan's Theorem: not (a or b) == not a and not b
    return {i: getattr(obj, i) for i in dir(obj) if not
            (i.startswith("__") or callable(getattr(obj, i)))}




def get_methods(obj):
    # Returns all methods of an object as a list
    # Dan Boschen 10/19/2020
    return [i for i in dir(obj) if not
            i.startswith("__") and callable(getattr(obj, i))]

