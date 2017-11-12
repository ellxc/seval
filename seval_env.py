import datetime
import itertools
import json
import math
import random
import re
import sys
import unicodedata
from base64 import b64encode, b64decode
from collections import Counter, namedtuple
from sys import getrecursionlimit

SevalEnv = {
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
    "range"      : range,
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
    "json"       : json,
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
    "sys"        : sys,
    "a"          : getrecursionlimit,
}

SevalEnv["env"] = SevalEnv
