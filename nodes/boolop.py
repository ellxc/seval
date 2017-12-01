import ast
from collections import namedtuple

from .evals import str_expr, eval_expr


def and_(env, node):
    for x in iter(node.values):
        x = eval_expr(env, x)
        if not x:
            return x
    return x


def or_(env, node):
    for x in iter(node.values):
        x = eval_expr(env, x)
        if x:
            return x
    return x


BoolOp = namedtuple('BoolOp', ['evaluate', 'pprint'])

boolops = {
    ast.And: BoolOp(
        evaluate=and_,
        pprint=lambda node: "(" + " and ".join(map(str_expr, node.values)) + ")"
    ),

    ast.Or : BoolOp(
        evaluate=or_,
        pprint=lambda node: "(" + " or ".join(str_expr(val) for val in node.values) + ")"
    ),
}
