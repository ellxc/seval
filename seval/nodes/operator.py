import ast
from collections import namedtuple
from collections.abc import Iterable

from .evals import str_expr, eval_expr

BinOp = namedtuple('BinOp', ['evaluate', 'pprint'])


def is_number(x):
    return isinstance(x, (int, float, complex)) and not isinstance(x, bool)


def power(env, a, b):
    a = eval_expr(env, a)
    b = eval_expr(env, b)
    if is_number(a) and a > 1000000 or is_number(b) and b > 10000:
        raise Exception("POW operator exceeds value limits")
    return a ** b


def multiply(env, a, b):
    a = eval_expr(env, a)
    b = eval_expr(env, b)
    if isinstance(a, Iterable) and is_number(b) and b > 1000:
        raise Exception("iterable building too large")
    return a*b

operators = {
    ast.Add     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) + eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '+' + str_expr(b),
    ),

    ast.Sub     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) - eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '-' + str_expr(b),
    ),

    ast.Mult    : BinOp(
        evaluate=multiply,
        pprint=lambda a, b: str_expr(a) + '*' + str_expr(b),
    ),

    ast.Div     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) / eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '/' + str_expr(b),
    ),

    ast.Mod     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) % eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '%' + str_expr(b)
    ),

    ast.Pow     : BinOp(
        evaluate=power,
        pprint=lambda a, b: str_expr(a) + '**' + str_expr(b)
    ),

    ast.LShift  : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) << eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '<<' + str_expr(b)
    ),

    ast.RShift  : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) >> eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '>>' + str_expr(b)
    ),

    ast.BitOr   : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) | eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '|' + str_expr(b)
    ),

    ast.BitXor  : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) ^ eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '^' + str_expr(b)
    ),

    ast.BitAnd  : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) & eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '&' + str_expr(b)
    ),

    ast.FloorDiv: BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) // eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '//' + str_expr(b)
    ),
}
