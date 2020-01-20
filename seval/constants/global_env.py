import datetime
import itertools
import json
import math
import random
import re
import unicodedata
from base64 import b64encode, b64decode
from collections import Counter, namedtuple, ChainMap
import os
import base64

def _range(*args):
    if len(args) == 1:
        stop = args[0]
        start = 0
        step = 1
    elif len(args) ==2:
        start = args[0]
        stop = args[1]
        step = 1
    elif len(args) ==3:
        start = args[0]
        stop = args[1]
        step = args[2]
    else:
        raise Exception("incorrect usage of range")

    if (abs(stop-step))/step >=1000:
        raise Exception("range used with too large numbers")

    return range(start, stop, step)


globalenv = ChainMap({
    "itertools"  : itertools,
    "abs"        : abs,
    "all"        : all,
    "any"        : any,
    "ascii"      : ascii,
    "bin"        : bin,
    "bool"       : bool,
    "callable"   : callable,
    "chr"        : chr,
    "complex"    : complex,
    "dict"       : dict,
    "dir"        : dir,
    "divmod"     : divmod,
    "enumerate"  : enumerate,
    "filter"     : filter,
    "float"      : float,
    "format"     : format,
    "hasattr"    : hasattr,
    "hash"       : hash,
    "hex"        : hex,
    "isinstance" : isinstance,
    "issubclass" : issubclass,
    "iter"       : iter,
    "int"        : int,
    "len"        : len,
    "list"       : list,
    "map"        : map,
    "max"        : max,
    "min"        : min,
    "next"       : next,
    "oct"        : oct,
    "ord"        : ord,
    "pow"        : pow,
    "range"      : _range,
    "repr"       : repr,
    "reversed"   : reversed,
    "round"      : round,
    "set"        : set,
    "slice"      : slice,
    "sorted"     : sorted,
    "str"        : str,
    "sum"        : sum,
    "tuple"      : tuple,
    "type"       : type,
    "zip"        : zip,
    "Counter"    : Counter,
    "sin"        : math.sin,
    "cos"        : math.cos,
    "tan"        : math.tan,
    "pi"         : math.pi,
    "math"       : math,
    "random"     : random,
    "datetime"   : datetime.datetime,
    "date"       : datetime.date,
    "time"       : datetime.time,
    "timedelta"  : datetime.timedelta,
    "timestamp"  : datetime.datetime.fromtimestamp,
    "re"         : re,
    "Exception"  : Exception,
    "unicodedata": unicodedata,
    "b64"        : namedtuple('base64', ('b64encode', 'b64decode'))(b64encode, b64decode),
    "print"      : (lambda *x: print(*x)),
    "os" : os,
    "base64": base64,
    "dict_with_os": {"os":os},
    "external_function": (lambda x: x()),
})

