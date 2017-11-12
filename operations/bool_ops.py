import ast
from collections import namedtuple


def and_(env, eval_fn, values):
    for x in iter(values):
        x = eval_fn(x, env)
        if not x:
            return x
    return x


def or_(env, eval_fn, values):
    for x in iter(values):
        x = eval_fn(x, env)
        if x:
            return x
    return x


BoolOp = namedtuple('BoolOp', ['evaluate', 'pprint'])

boolops = {
    ast.And: BoolOp(
        evaluate=and_,
        pprint=lambda str_fn, values: "(" + " and ".join(map(str_fn, values)) + ")"
    ),

    ast.Or : BoolOp(
        evaluate=or_,
        pprint=lambda str_fn, values: "(" + " or ".join(map(str_fn, values)) + ")"
    ),
}
